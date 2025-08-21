import hashlib
import re
from typing import Optional

from extractors.regex_extractor import extract_salary, extract_email, extract_telegram_username, extract_url
from extractors.ner_extractor import extract_ner_fields
from extractors.tagger import extract_tags
from extractors.bulk_llm_extractor import extract_jobs_with_bulk_llm
from helper.config import ConfigSingleton
from helper.logger import Logger
from models.job_models.job import Job

class JobExtractorService:
    def __init__(self):
        self.logger = Logger(__name__)
        self.config = ConfigSingleton()

    def _is_potentially_complex(self, text: str, links: list) -> bool:
        """
        Applies heuristics to check if a job posting is too complex for simple extraction.
        """
        # Check 1: More than one link often confuses simple link extractors.
        if len(links) > 1:
            self.logger.debug("Flagged as complex: Multiple links found.")
            return True

        # Check 2: The text contains salary-like patterns (e.g., "$", "€", "salary")
        # but the regex extractor failed to pull out a structured salary.
        salary_keywords = ['salary', 'pay', 'compensation', '$', '€', '£']
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in salary_keywords) and not extract_salary(text):
            self.logger.debug("Flagged as complex: Potential salary missed by regex.")
            return True

        return False

    def _extract_simple_fields(self, message: dict) -> (dict, bool):
        """
        Performs the initial, fast extraction using Regex and NER.
        Returns the extracted data and a boolean indicating if it's complex.
        """
        text = message['text']

        # Basic field extraction
        ner_fields = extract_ner_fields(text)
        title = ner_fields.get("title")
        company = ner_fields.get("company")

        # Heuristic checks for complexity
        links = re.findall(r'https?://[^\s\)]+', text)
        is_complex = self._is_potentially_complex(text, links)
        if not (title and company and links):
            is_complex = True

        simple_data = {
            "title": title,
            "company": company,
            "location": ner_fields.get("location"),
            "salary": extract_salary(text),
            "link": links[0] if links else None,
            "contact": extract_email(text) or extract_telegram_username(text),
            "description": text,
            "date_posted": message.get('date', ""),
            "source": "telegram"
        }

        return simple_data, is_complex

    def process_messages_in_batches(self, messages: list[dict]) -> list[Job]:
        simple_jobs = []
        complex_job_texts = []

        self.logger.info("Starting extraction process...")
        for message in messages:
            if not message.get('text'):
                continue

            # Attempt simple extraction first
            job_data, is_complex = self._extract_simple_fields(message)

            if is_complex:
                # If complex, add the raw text to a list for the LLM
                complex_job_texts.append(message['text'])
            else:
                # If simple, process it immediately
                job_obj = self._create_job_object(job_data)
                if job_obj:
                    simple_jobs.append(job_obj)

        llm_extracted_jobs = []
        if complex_job_texts:
            print(complex_job_texts)
            llm_results = extract_jobs_with_bulk_llm(self.config.hugging_face_api, complex_job_texts)
            for job_data in llm_results:
                job_obj = self._create_job_object(job_data)
                if job_obj:
                    llm_extracted_jobs.append(job_obj)

        self.logger.info(f"Processed {len(simple_jobs)} simple jobs and {len(llm_extracted_jobs)} complex jobs.")
        return simple_jobs + llm_extracted_jobs

    def _create_job_object(self, job_data: dict) -> Optional[Job]:

        if not (job_data.get("title") and job_data.get("company")):
            return None

        # Generate tags and the job hash
        full_text = job_data.get("description", "") or job_data.get("title", "")
        job_data["tags"] = extract_tags(full_text)
        job_data["job_hash"] = self._generate_job_hash(job_data)
        return Job(**job_data)

    def _generate_job_hash(self, job_fields: dict) -> str:
        base_str = (
                (job_fields.get("title") or "").lower().strip() + "|" +
                (job_fields.get("company") or "").lower().strip() + "|" +
                (job_fields.get("link") or "").lower().strip()
        )
        return hashlib.sha256(base_str.encode()).hexdigest()
import hashlib
import re
from extractors.regex_extractor import (
    extract_url, extract_salary, extract_email, extract_telegram_username, extract_special_location_keywords
)
from extractors.ner_extractor import extract_ner_fields
from extractors.llm_extractor import extract_with_llm
from extractors.tagger import extract_tags
from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from helper import ConfigSingleton
from helper.logger import Logger
from models.job import Job

class JobExtractorService:
    def __init__(self):
        self.logger = Logger(__name__)
        self.telegram_group_fetcher = TelegramGroupFetcher()
        self.config = ConfigSingleton()

    def clean_text(self, text):
        text = re.sub(r"[^\w\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def is_potential_job_posting(self, text):
        cleaned = self.clean_text(text)
        if len(cleaned) < 40:
            return False
        job_keywords = [
            "hiring", "position", "vacancy", "role", "developer", "engineer",
            "job", "opening", "opportunity", "career", "apply", "join our team"
        ]
        cleaned_lower = cleaned.lower()
        if not any(word in cleaned_lower for word in job_keywords):
            return False
        return True

    def generate_job_hash(self, job_fields):
        # Hash based on normalized title, company, link, location
        base_str = (
            (job_fields.get("title") or "").lower().strip() + "|" +
            (job_fields.get("company") or "").lower().strip() + "|" +
            (job_fields.get("link") or "").lower().strip() + "|" +
            (job_fields.get("location") or "").lower().strip()
        )
        return hashlib.sha256(base_str.encode()).hexdigest()

    def extract_job_fields(self, message):
        text = message['text']

        if not self.is_potential_job_posting(text):
            return None

        links = self.telegram_group_fetcher.extract_all_links(message)
        link = links[0] if links else None

        email = extract_email(text)
        telegram_contact = extract_telegram_username(text)
        contact = email or telegram_contact

        salary = extract_salary(text)
        ner_fields = extract_ner_fields(text)
        if not ner_fields['company'] or not ner_fields['title']:
            llm_fields = extract_with_llm(text, self.config.openrouter_api_key)
            company = llm_fields['company'] or ner_fields['company']
            if not (company and company.strip()):
                return None
            title = llm_fields['title'] or ner_fields['title']
            location = llm_fields['location'] or ner_fields['location']
            special_locs = extract_special_location_keywords(text)
            if special_locs:
                if location:
                    # If NER location exists, combine them
                    # Avoid duplicates: don't append "Remote" if already present in location
                    special = ", ".join([loc for loc in special_locs if loc.lower() not in location.lower()])
                    if special:
                        location = f"{location}, {special}"
                else:
                    location = ", ".join(special_locs)
        else:
            company = ner_fields['company']
            title = ner_fields['title']
            location = ner_fields['location']

        if not (title and company):
            return None

        tags = extract_tags(text)
        cleaned_text = re.sub(r'[\n\r]+', ' ', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        # --- Calculate job hash
        job_fields = {
            "title": title,
            "company": company,
            "link": link or "",
            "location": location or "",
        }
        job_hash = self.generate_job_hash(job_fields)

        return Job(
            title=title,
            company=company,
            link=link,
            contact=contact,
            description=cleaned_text,
            date_posted=message.get('date', ""),
            location=location,
            salary=salary,
            tags=tags,
            job_hash=job_hash
        )

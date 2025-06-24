# services/job_extractor_service.py

from extractors.regex_extractor import extract_url, extract_salary
from extractors.ner_extractor import extract_ner_fields
from extractors.llm_extractor import extract_with_llm
from models.job import Job

class JobExtractorService:
    def __init__(self):
        pass  # If you need to initialize anything

    def extract_job_fields(self, message):
        text = message['text']
        link = extract_url(text)
        salary = extract_salary(text)
        ner_fields = extract_ner_fields(text)
        # Fallback to LLM
        if not ner_fields['company'] or not ner_fields['title']:
            llm_fields = extract_with_llm(text)
            company = llm_fields['company'] or ner_fields['company']
            title = llm_fields['title'] or ner_fields['title']
            location = llm_fields['location'] or ner_fields['location']
        else:
            company = ner_fields['company']
            title = ner_fields['title']
            location = ner_fields['location']

        if not (title and company and link):
            return None

        job = Job(
            title=title,
            company=company,
            link=link,
            description=text,
            date_posted=message.get('date', ""),
            location=location,
            salary=salary
        )
        return job

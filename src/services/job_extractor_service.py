import re
from extractors.regex_extractor import extract_url, extract_salary
from extractors.ner_extractor import extract_ner_fields
from extractors.llm_extractor import extract_with_llm
from models.job import Job

class JobExtractorService:
    def clean_text(self, text):
        """
        Removes special characters and extra spaces.
        Leaves alphanumerics and spaces only.
        """
        # Remove all non-alphanumeric except spaces (preserve URLs if needed)
        text = re.sub(r"[^\w\s]", " ", text)
        # Collapse multiple spaces to one
        return re.sub(r"\s+", " ", text).strip()

    def is_potential_job_posting(self, text):
        """
        Quickly checks if the text is likely a job post.
        Returns True if it should be further processed.
        """
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
        if not extract_url(text):  # use original text for URL
            return False
        return True

    def extract_job_fields(self, message):
        text = message['text']

        if not self.is_potential_job_posting(text):
            return None

        link = extract_url(text)
        salary = extract_salary(text)
        ner_fields = extract_ner_fields(text)
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

        return Job(
            title=title,
            company=company,
            link=link,
            description=text,
            date_posted=message.get('date', ""),
            location=location,
            salary=salary
        )

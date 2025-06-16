# main.py
from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from extractors.regex_extractor import extract_url, extract_salary
from extractors.ner_extractor import extract_ner_fields
from extractors.llm_extractor import extract_with_llm
from models.job import Job

def extract_job_fields(message):
    text = message['text']
    # 1. Regex for link, salary
    link = extract_url(text)
    salary = extract_salary(text)
    # 2. NER for company, title, location
    ner_fields = extract_ner_fields(text)
    # 3. Fallback: if title or company missing, use LLM
    if not ner_fields['company'] or not ner_fields['title']:
        llm_fields = extract_with_llm(text)
        company = llm_fields['company'] or ner_fields['company']
        title = llm_fields['title'] or ner_fields['title']
        location = llm_fields['location'] or ner_fields['location']
    else:
        company = ner_fields['company']
        title = ner_fields['title']
        location = ner_fields['location']
    # Build Job object
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

if __name__ == "__main__":
    fetcher = TelegramGroupFetcher(groups_path='resources/groups.json')
    messages = fetcher.fetch_last_24_hours()
    jobs = [extract_job_fields(msg) for msg in messages]
    # Example: print structured jobs
    for job in jobs:
        print(job.json(indent=2))

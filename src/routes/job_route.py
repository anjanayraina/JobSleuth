# routes/jobs.py
from fastapi import APIRouter, Query , Body
from services.jobs_service import get_jobs_service
from fastapi import APIRouter
from services.job_extractor_service import JobExtractorService
from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from extractors.tagger import extract_tags
from helper.db import MongoDB
from helper.logger import Logger
from datetime import datetime
from typing import List
from models.job import Job
from models.extract_job_request import ExtractJobsRequest
router = APIRouter()
extractor = JobExtractorService()
db = MongoDB()
log = Logger()

@router.post("/trigger_fetch_jobs")
async def trigger_fetch_jobs():
    fetcher = TelegramGroupFetcher()
    messages = await fetcher.fetch_messages()
    log.info(f"Manually triggered: Fetched {len(messages)} messages.")

    inserted = 0
    for message in messages:
        job_obj = extractor.extract_job_fields(message)
        if job_obj:
            job_dict = job_obj.dict()
            job_dict["tags"] = extract_tags(job_obj.description)
            job_dict["source"] = "telegram"
            job_dict["fetched_at"] = datetime.utcnow().isoformat()
            db.insert_job(job_dict)
            inserted += 1
            log.info(f"Inserted job: {job_obj.title} at {job_obj.company}")

    return {"status": "success", "inserted_jobs": inserted}

@router.get("/jobs")
def get_jobs(tags: str = Query(default=None)):
    return get_jobs_service(tags)

@router.get("/fetch_extracted_jobs", response_model=List[Job])
async def fetch_extracted_jobs():
    """
    Fetches latest Telegram group messages, extracts job objects,
    and returns a list of structured job postings (not saved to DB).
    """
    fetcher = TelegramGroupFetcher()
    messages = await fetcher.fetch_messages()
    jobs = []
    for message in messages:
        job_obj = extractor.extract_job_fields(message)
        if job_obj:
            jobs.append(job_obj)
    log.info(f"Fetched and extracted {len(jobs)} jobs (not saved to DB).")
    return jobs

@router.post("/extract_jobs", response_model=List[Job])
async def extract_jobs_from_texts(request: ExtractJobsRequest):
    jobs = []
    for text in request.texts:
        message = {"text": text}
        job = extractor.extract_job_fields(message)
        if job:
            jobs.append(job)
    return jobs

from fastapi import APIRouter
from services.jobs_service import get_jobs_service
from services.job_extractor_service import JobExtractorService
from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from services.mongodb_service import MongoDBService
from helper.logger import Logger
from typing import List
from models.job_models.job import Job
from models.job_models.extract_job_request import ExtractJobsRequest

router = APIRouter()
log = Logger(__name__)
extractor = JobExtractorService()
db = MongoDBService()


@router.post("/trigger_fetch_jobs")
async def trigger_fetch_jobs():
    fetcher = TelegramGroupFetcher()
    messages = await fetcher.fetch_messages()
    log.info(f"Manually triggered: Fetched {len(messages)} messages.")

    inserted_count = 0
    for message in messages:
        job_obj = extractor.extract_job_fields(message)
        if job_obj:
            job_dict = job_obj.model_dump()
            db.insert_job(job_dict)
            inserted_count += 1
            log.info(f"Inserted job: {job_obj.title}")

    return {"status": "success", "inserted_jobs": inserted_count}


@router.get("/jobs", response_model=List[Job])
def get_jobs():
    log.info(f"Request received for jobs")
    return get_jobs_service()

@router.get("/fetch_extracted_jobs", response_model=List[Job])
async def fetch_extracted_jobs():
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
        message = {"text": text, "date": "placeholder_date"}
        job = extractor.extract_job_fields(message)
        if job:
            jobs.append(job)
    return jobs

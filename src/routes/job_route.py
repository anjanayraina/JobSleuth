from http.client import HTTPException

from fastapi import APIRouter


from services.job_extractor_service import JobExtractorService
from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from services.mongodb_service import MongoDBService


from fastapi import APIRouter, Depends, Query, HTTPException
from services.jobs_service import get_jobs_service, get_job_by_id_service
from services.job_workflow_service import JobsWorkflowService
from models.job_models.job import Job
from models.job_models.job_response import JobResponse
from models.job_models.extract_job_request import ExtractJobsRequest
from models.user_models.user import User
from helper.security import get_current_user
from helper.logger import Logger
from typing import List
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


@router.get("/jobs", response_model=List[JobResponse])
def get_jobs():
    log.info(f"Request received for jobs")
    return get_jobs_service()


@router.get("/jobs/{job_id}", response_model=Job)
def get_single_job(job_id: str):
    log.info(f"Request received for job with ID: {job_id}")
    job = get_job_by_id_service(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.post("/run-workflow", status_code=200)
async def run_job_workflow(current_user: User = Depends(get_current_user)):
    """
    Triggers the entire workflow to fetch, process, and store new jobs.
    This endpoint is protected and requires authentication.
    """
    log.info(f"Job workflow triggered by user: {current_user.email}")
    workflow_service = JobsWorkflowService()
    try:
        inserted_count = await workflow_service.run_workflow()
        return {"status": "success", "new_jobs_inserted": inserted_count}
    except Exception as e:
        log.error(f"An error occurred during the workflow: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during the workflow.")
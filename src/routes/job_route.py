from http.client import HTTPException

from fastapi import APIRouter, Depends, Query, HTTPException

# Import the response model for pagination
from models.job_models.paginated_job_response import PaginatedJobResponse
from services.job_extractor_service import JobExtractorService
from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from services.mongodb_service import MongoDBService
from services.jobs_service import get_jobs_service, get_job_by_id_service, get_latest_jobs_service, get_jobs_service_paginated
from services.job_workflow_service import JobsWorkflowService
from models.job_models.job import Job
from models.job_models.job_response import JobResponse
from models.job_models.extract_job_request import ExtractJobsRequest
from models.user_models.user import User
from helper.security import get_current_user, get_current_admin_user  # We use get_current_user
from helper.logger import Logger
from typing import List

router = APIRouter()
log = Logger(__name__)
extractor = JobExtractorService()
db = MongoDBService()



@router.get("/jobs", response_model=List[JobResponse], tags=["Jobs"])
def get_jobs(current_user: User = Depends(get_current_user)):
    """(Protected) Gets all jobs from the database (non-paginated)."""
    log.info(f"Request for all jobs received from user: {current_user.email}")
    return get_jobs_service()



@router.post("/run-workflow", status_code=200 , tags=["admin"])
async def run_job_workflow(current_admin: User = Depends(get_current_admin_user)):
    log.info(f"Job workflow triggered by ADMIN user: {current_admin.email}")
    workflow_service = JobsWorkflowService()
    try:
        inserted_count = await workflow_service.run_workflow()
        return {"status": "success", "new_jobs_inserted": inserted_count}
    except Exception as e:
        log.error(f"An error occurred during the workflow: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during the workflow.")


@router.get("/jobs/latest", response_model=List[JobResponse], tags=["Jobs"])
def get_latest_jobs(limit: int = Query(10, gt=0, le=100, description="Number of latest jobs to fetch"), current_user: User = Depends(get_current_user)):
    """(Protected) Fetches the N most recent jobs."""
    log.info(f"Request for latest jobs received from user: {current_user.email}")
    try:
        jobs = get_latest_jobs_service(limit)
        return jobs
    except Exception as e:
        log.error(f"Failed to fetch latest jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch latest jobs.")


@router.get("/health", status_code=200, tags=["Health"])
def health_check():
    """(Public) A simple endpoint to check if the API is running."""
    log.info("Health check endpoint was called.")
    return {"status": "ok", "message": "API is healthy"}


@router.get("/jobs/paginated", response_model=PaginatedJobResponse, tags=["Jobs"])
def get_jobs_paginated(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), current_user: User = Depends(get_current_user)):
    """(Protected) Gets a paginated list of jobs from the database."""
    log.info(f"Paginated job request from {current_user.email} with skip: {skip}, limit: {limit}")
    paginated_result = get_jobs_service_paginated(skip=skip, limit=limit)
    return paginated_result
# routes/job_search.py
from fastapi import APIRouter
from models.job_search_request import JobSearchRequest
from services.job_search_service import JobSearchService

router = APIRouter()
search_service = JobSearchService()

@router.post("/search_jobs")
def search_jobs(request: JobSearchRequest):
    results = search_service.search_jobs(request)
    return results

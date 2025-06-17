# routes/jobs.py
from fastapi import APIRouter, Query
from services.jobs_service import get_jobs_service

router = APIRouter()

@router.get("/jobs")
def get_jobs(tags: str = Query(default=None)):
    return get_jobs_service(tags)

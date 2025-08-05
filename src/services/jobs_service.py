# src/services/jobs_service.py
from services.mongodb_service import MongoDBService
from models.job_models.job_response import JobResponse
from models.job_models.job import  Job

from typing import List, Optional


def get_jobs_service(tags: str = None) -> List[Job]:
    db = MongoDBService()
    query = {}
    if tags:
        query["tags"] = {"$in": tags.split(",")}

    raw_jobs = db.find_jobs(query)

    processed_jobs = []
    for job_data in raw_jobs:
        job_data["id"] = str(job_data["_id"])
        del job_data["_id"]
        processed_jobs.append(job_data)
    jobs = [JobResponse.model_validate(job) for job in processed_jobs]

    return jobs


def get_job_by_id_service(job_id: str) -> Optional[JobResponse]:
    """Gets a single job by its ID and validates it with the response model."""
    db = MongoDBService()
    raw_job = db.find_job_by_id(job_id)

    if raw_job:
        # If a job is found, we validate it with our response model.
        # This correctly handles the conversion of '_id' to 'id'.
        return JobResponse.model_validate(raw_job)

    # If no job is found, we return None.
    return None
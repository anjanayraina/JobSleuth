# src/services/jobs_service.py
from services.mongodb_service import MongoDBService
from models.job_models.job_response import JobResponse
from models.job_models.job import  Job

from typing import List


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
    jobs = [Job.model_validate(job) for job in processed_jobs]

    return jobs

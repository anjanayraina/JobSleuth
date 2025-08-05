# src/services/jobs_service.py
from services.mongodb_service import MongoDBService
from models.job_models.job import Job
from typing import List


def get_jobs_service() -> List[Job]:

    db = MongoDBService()
    query = {}

    raw_jobs = db.find_jobs(query)

    jobs = [Job.model_validate(job) for job in raw_jobs]

    return jobs

from pydantic import BaseModel
from typing import List
from src.models.job_models.job import Job

class PaginatedJobResponse(BaseModel):
    total: int
    jobs: List[Job]
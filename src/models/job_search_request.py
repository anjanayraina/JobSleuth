# models/job_search.py
from typing import List, Optional
from pydantic import BaseModel

class JobSearchRequest(BaseModel):
    general_query: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    company: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    limit: int = 10
    skip: int = 0

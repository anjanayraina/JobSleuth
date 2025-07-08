from pydantic import BaseModel
from typing import Optional, List

class Job(BaseModel):
    title: str
    company: str
    description: str
    job_hash: str = ""
    date_posted: Optional[str] = ""
    location: Optional[str] = ""
    salary: Optional[str] = ""
    link: Optional[str] = None
    contact: Optional[str] = None
    tags: Optional[List[str]] = []
    source: Optional[str] = "telegram"
    fetched_at: Optional[str] = None
    job_type: Optional[str] = None

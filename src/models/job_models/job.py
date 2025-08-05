from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

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
    fetched_at: datetime = Field(default_factory=datetime.now)
    job_type: Optional[str] = None

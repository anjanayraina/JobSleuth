from pydantic import BaseModel
from typing import Optional

class Job(BaseModel):
    title: str
    company: str
    link: str
    description: str
    date_posted: Optional[str] = ""
    location: Optional[str] = ""
    salary: Optional[str] = ""
    tags: Optional[list] = []
    source: Optional[str] = ""
    fetched_at: Optional[str] = ""

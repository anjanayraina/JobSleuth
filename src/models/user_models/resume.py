from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date

class WorkExperience(BaseModel):
    """Represents a single entry of work experience from a resume."""
    job_title: str
    company: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

class Education(BaseModel):
    """Represents a single entry of education from a resume."""
    institution: str
    degree: str
    field_of_study: str
    graduation_date: Optional[date] = None

class ResumeData(BaseModel):
    """A structured representation of data extracted from a user's resume."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    work_experience: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    summary: Optional[str] = None

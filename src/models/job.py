from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId  # Import ObjectId from the MongoDB driver

# This helper class is essential. It teaches Pydantic how to handle
# MongoDB's specific ObjectId type during validation and JSON conversion.
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
         schema.update(type="string")
         return schema

# This is your new Job model with the ObjectId fix integrated.
class Job(BaseModel):
    # This 'id' field maps to MongoDB's '_id' and handles the conversion.
    # It's the key to fixing the error.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    # --- Your requested model structure ---
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
    # We use default_factory for fields that should be set on creation.
    fetched_at: datetime = Field(default_factory=datetime.now)
    job_type: Optional[str] = None
    # ------------------------------------

    class Config:
        # These settings are required for Pydantic to work with MongoDB objects.
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str  # This tells FastAPI to convert ObjectId to a string in JSON responses.
        }
        json_schema_extra = {
            "example": {
                "id": "60d5ec49e77e8b2b5a8e3f7a",
                "title": "Backend Developer",
                "company": "Sleuth Inc.",
                "description": "Looking for a developer skilled in Python.",
                "job_hash": "a1b2c3d4e5f6",
                "date_posted": "2024-07-31",
                "location": "Remote",
                "salary": "$95,000",
                "link": "https://t.me/jobs/12345",
                "tags": ["python", "backend", "fastapi"],
                "source": "telegram",
                "fetched_at": "2024-07-31T13:52:00Z",
                "job_type": "Full-time"
            }
        }

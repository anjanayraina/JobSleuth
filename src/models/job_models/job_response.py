from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models.job_models.job import Job

class JobResponse(Job):
    id: str

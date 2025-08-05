from pydantic import BaseModel
from typing import List

class ExtractJobsRequest(BaseModel):
    texts: List[str]

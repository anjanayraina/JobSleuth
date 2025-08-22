from pydantic import BaseModel, EmailStr
from models.user_models.subscription import Subscription
from models.user_models.resume import ResumeData
from typing import Optional , List
from pydantic import Field

class User(BaseModel):
    email: EmailStr
    disabled: bool = False
    username: str
    email: EmailStr
    hashed_password: str
    subscription: Subscription = Subscription.FREE
    liked_jobs: List[str] = Field(default_factory=list)
    saved_jobs: List[str] = Field(default_factory=list)
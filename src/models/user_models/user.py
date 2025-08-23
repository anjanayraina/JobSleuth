from pydantic import BaseModel, EmailStr

from models.user_models.role import Role
from models.user_models.subscription import Subscription
from models.user_models.resume import ResumeData
from typing import Optional , List
from pydantic import Field

class User(BaseModel):

    username: str
    email: EmailStr
    disabled: bool = False
    subscription: Subscription = Subscription.FREE
    liked_jobs: List[str] = Field(default_factory=list)
    saved_jobs: List[str] = Field(default_factory=list)
    role: Role = Role.USER
    resume_data: Optional[ResumeData] = None
    hashed_password: str
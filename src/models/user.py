from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import Field

class User(BaseModel):
    username : str = ""
    email: EmailStr
    disabled: bool = False
class UserInDB(User):
    hashed_password: str

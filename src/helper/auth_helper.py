from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from helper.config import ConfigSingleton

config = ConfigSingleton()
SECRET_KEY = config.jwt_secret_key
ALGORITHM = config.jwt_algorithm

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

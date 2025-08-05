from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from helper.config import ConfigSingleton
from services.mongodb_service import MongoDBService
from models.user_models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

config = ConfigSingleton()
SECRET_KEY = config.jwt_secret_key
ALGORITHM = config.jwt_algorithm


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = MongoDBService()
    user_data = db.get_user_by_email(email)
    if user_data is None:
        raise credentials_exception

    user = User(**user_data)
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

from services.mongodb_service import MongoDBService
from helper.password import verify_password, get_password_hash
from helper.auth_helper import create_access_token
from models.user import User, UserInDB
from helper.logger import Logger

router = APIRouter(prefix="/auth", tags=["Authentication"])
log = Logger(__name__)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/signup")
def signup(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db = MongoDBService()
    user = db.get_user_by_email(form_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(form_data.password)
    user_data = {"email": form_data.username, "hashed_password": hashed_password}
    db.create_user(user_data)

    log.info(f"New user signed up: {form_data.username}")
    return {"message": "User created successfully. Please log in."}


@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db = MongoDBService()
    user_data = db.get_user_by_email(form_data.username)

    if not user_data or not verify_password(form_data.password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserInDB(**user_data)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    log.info(f"User logged in: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}

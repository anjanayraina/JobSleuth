from fastapi import APIRouter, HTTPException, status
from datetime import timedelta

from services.mongodb_service import MongoDBService
from helper.password import verify_password, get_password_hash
from helper.auth_helper import create_access_token
from models.user_models.user import User
from models.user_models.login_request import LoginRequest
from helper.logger import Logger

router = APIRouter(prefix="/auth", tags=["Authentication"])
log = Logger(__name__)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/signup")
def signup(login_data: LoginRequest): # Use the LoginRequest model for signup as well
    db = MongoDBService()
    if db.get_user_by_email(login_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(login_data.password)
    user_data = {"email": login_data.email, "hashed_password": hashed_password}
    db.create_user(user_data)

    log.info(f"New user signed up: {login_data.email}")
    return {"message": "User created successfully. Please log in."}

@router.post("/token")
def login_for_access_token(login_data: LoginRequest):
    db = MongoDBService()
    # The username and password now come from the Pydantic model
    user_data = db.get_user_by_email(login_data.email)

    if not user_data or not verify_password(login_data.password, user_data.get("hashed_password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = User(**user_data)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    log.info(f"User logged in: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}

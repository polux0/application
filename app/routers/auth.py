from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

# Constants for JWT token creation
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.

    Args:
    - user (UserCreate): UserCreate schema object.
    - db (Session): Database session.

    Returns:
    - User: Created User object.

    Raises:
    - HTTPException: If the email is already registered.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.post("/login")
def login(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user and return a JWT token.

    Args:
    - form_data (UserCreate): UserCreate schema object.
    - db (Session): Database session.

    Returns:
    - dict: Access token and token type.

    Raises:
    - HTTPException: If the email or password is incorrect.
    """
    user = crud.get_user_by_email(db, email=form_data.email)
    if not user or user.hashed_password != form_data.password + "notreallyhashed":
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT token.

    Args:
    - data (dict): Data to include in the token.
    - expires_delta (timedelta, optional): Token expiration time.

    Returns:
    - str: Encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

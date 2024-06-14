from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from jose import JWTError, jwt
from app import crud

# Constants for JWT token creation
SECRET_KEY = "secret"
ALGORITHM = "HS256"

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    """
    Dependency to get a new database session.

    Yields:
    - db (Session): Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency to get the current authenticated user based on JWT token.

    Args:
    - token (str): JWT token from the Authorization header.
    - db (Session): Database session.

    Returns:
    - User: Authenticated User object.

    Raises:
    - HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=401,
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
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

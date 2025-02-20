from fastapi import HTTPException, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session
from alembic.models.endpoints.user import User
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from db_session_provider import get_db_session

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.timezone.utc() + expires_delta
    else:
        expire = datetime.timezone.utc() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str Depends):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(verify_token), db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def get_current_admin(token: str = Depends(verify_token), db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == token).first()
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

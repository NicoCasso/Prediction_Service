from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from passlib.context import CryptContext
import jwt

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

from sqlalchemy.orm import Session
from models.models import UserInDb
from schemas.auth_data import Token


from db.session_provider import get_db_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES//2)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str) :
    """
    raise HTTP_401_UNAUTHORIZED Exception
    """
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.PyJWTError :
        raise credentials_exception
    
    if payload is None : 
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    return payload


def get_current_user(payload, db_session : Session) -> UserInDb :
    """
    raise HTTP_401_UNAUTHORIZED or HTTP_403_FORBIDDEN Exception
    """
    data_email = payload.get("sub")
    data_id = payload.get("id")
    user = db_session.query(UserInDb).filter(UserInDb.id == data_id).first()

    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found")
    
    if not user.is_active : 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions")
    
    return user

def get_current_admin(payload, db_session : Session) -> UserInDb :
    """
    raise HTTP_403_FORBIDDEN Exception
    """
    data_email = payload.get("sub")
    data_id = payload.get("id")
    user = db_session.query(UserInDb).filter(UserInDb.id == data_id).first()
    
    if not user or not user.is_active or user.role != "admin" :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions")
    
    return user


from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional

# application imports
from models.models import UserInDb

def get_current_user(payload, db_session : Session, need_activated_user:bool = True) -> UserInDb :
    """
    raise HTTP_404_NOT_FOUND or HTTP_401_UNAUTHORIZED Exception
    """
    data_email = payload.get("sub")
    data_id = payload.get("id")
    user = db_session.query(UserInDb).filter(UserInDb.id == data_id).first()

    raise_user_exceptions(need_activated_user, user)
    
    return user

def get_current_admin(payload, db_session : Session, need_activated_user:bool = True) -> UserInDb :
    """
    raise HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED or HTTP_403_FORBIDDEN Exception
    """
    data_email = payload.get("sub")
    data_id = payload.get("id")
    user = db_session.query(UserInDb).filter(UserInDb.id == data_id).first()
    
    raise_user_exceptions(need_activated_user, user)

    if user.role != "admin" :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions")
    
    return user

def raise_user_exceptions(need_activated_user: bool, user : Optional[UserInDb]):
    if not user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found")
    
    if need_activated_user :
        if not user.is_active : 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="User not activated")


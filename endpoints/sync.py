from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from sqlalchemy.orm import Session

# application imports
from core.password_tools import get_password_hash
from db.session_provider import get_db_session
from models.models import UserInDb
from schemas.users_data import UserInfoData, UserCreationData


router = APIRouter(tags=["sync"])

# Sync Django admin with FastApi Endpoint
@router.post("/users", response_model=UserInfoData)
def sync_user(
    creation_data: UserCreationData, 
    db_session: Session = Depends(get_db_session)
) -> UserInfoData:
    """
    Sync a user from Django to FastAPI.
    """
    # Check if the user already exists
    db_user = db_session.query(UserInDb).filter(UserInDb.email == creation_data.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    # Create the user
    db_user = UserInDb(email=creation_data.email)
    db_user.username = creation_data.username
    db_user.role = creation_data.role
    
    # Handle password hashing
    if creation_data.password.startswith("bcrypt$$"):
        db_user.password_hash = creation_data.password.replace("bcrypt$", "")  # Strip the prefix
    else:
        db_user.password_hash = get_password_hash(creation_data.password)  # Hash plaintext password
    
    db_user.is_active = True  # Admin users are active by default
    db_session.add(db_user)
    db_session.commit()
    
    return UserInfoData(
        email=db_user.email,
        username=db_user.username,
        is_active=db_user.is_active,
        role=db_user.role
    )

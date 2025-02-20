from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from alembic.models.endpoints.user import User
from alembic.models.endpoints.validation_models import UserCreationData
from dependencies import get_current_admin, get_db_session
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.schemas.user import UserRead
from app.utils.jwt_handler import verify_token


router = APIRouter()

#______________________________________________________________________________
#
# Liste des utilisateurs (Admin)
#______________________________________________________________________________
@router.get("/admin/users")
def get_users(current_user: str = Depends(get_current_admin), 
              session: Session = Depends(get_db_session)):
    
    users = session.exec(User).all()
    return {"users": users}

#______________________________________________________________________________
#
# region Création d'un utilisateur (Admin)
#______________________________________________________________________________
@router.post("/admin/users", response_model=User)
def create_user(user: UserCreationData, 
                current_user: str = Depends(get_current_admin), 
                session: Session = Depends(get_db_session)) -> User:
    
    db_user = User(email=user.email)
    db_user.set_password(user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

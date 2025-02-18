from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from validation_models import UserCreationData
from dependencies import get_current_admin, get_db_session

router = APIRouter()

#______________________________________________________________________________
#
# Liste des utilisateurs (Admin)
#______________________________________________________________________________
@router.get("/admin/users")
def get_users(current_user: str = Depends(get_current_admin), 
              session: Session = Depends(get_db_session)):
    
    users = session.query(User).all()
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

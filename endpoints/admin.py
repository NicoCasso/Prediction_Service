from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, UserCreate
from dependencies import get_current_admin, get_session

router = APIRouter()


#______________________________________________________________________________
#
# Liste des utilisateurs (Admin)
#______________________________________________________________________________
@router.get("/admin/users")
def get_users(current_user: str = Depends(get_current_admin), session: Session = Depends(get_session)):
    users = session.query(User).all()
    return {"users": users}

#______________________________________________________________________________
#
# Création d'un utilisateur (Admin)
#______________________________________________________________________________
@router.post("/admin/users", response_model=User)
def create_user(user: UserCreate, current_user: str = Depends(get_current_admin), session: Session = Depends(get_session)) -> User:
    db_user = User(username=user.username)
    db_user.set_password(user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

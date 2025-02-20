from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.models import UserInDb
from schemas.users_data import UserInfoData, UserCreationData
from typing import List

import core.password_management as pm 

from schemas.auth_data import Token
from utils.jwt_handlers import verify_token, get_current_admin
from db.session_provider import get_db_session


router = APIRouter()

admin_scheme = OAuth2PasswordBearer(tokenUrl="/admin/users")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)

#______________________________________________________________________________
#
# Liste des utilisateurs (Admin)
#______________________________________________________________________________
@router.get("/admin/users", response_model=List[UserInfoData])
def get_users(
    token : str  = Depends(admin_scheme), 
    session: Session = Depends(get_db_session)):
    
    payload = verify_token(token)
    if payload is None:
        raise unauthorised_exception
    
    db_admin = get_current_admin(payload, session)

    db_users = session.query(UserInDb).all()

    users_data = []
    for db_user in db_users :
        users_data.append(
            UserInfoData (
                email = db_user.email,
                username = db_user.username, 
                is_active= db_user.is_active,
                role = db_user.role))
        
    users_data : list[UserInfoData] = users_data
    return users_data

#______________________________________________________________________________
#
# region Création d'un utilisateur (Admin)
#______________________________________________________________________________
@router.post("/admin/users", response_model=UserInfoData)
def create_user(
    creation_data: UserCreationData, 
    token : str = Depends(admin_scheme), 
    db_session: Session = Depends(get_db_session)) -> UserInfoData:

    payload = verify_token(token)
    db_admin = get_current_admin(payload, db_session)

    if creation_data.role not in ["admin", "user"] :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ce rôle n'existe pas ")
    
    db_user = UserInDb(email=creation_data.email)
    db_user.username = creation_data.username
    db_user.password_hash = pm.get_password_hash(creation_data.email)
    db_user.is_active = creation_data.is_active
    db_user.role = creation_data.role
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)

    user_data : UserInfoData = creation_data
    return user_data

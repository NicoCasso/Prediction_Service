from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
#from sqlmodel import Session, select
from sqlalchemy.orm import Session
from typing import List

# application imports
from core.password_tools import get_password_hash
from core.user_role_tools import get_current_admin
from db.session_provider import get_db_session
from db.token_white_list import register_token, is_valid_token, invalidate_token
from models.models import UserInDb
from schemas.users_data import UserInfoData, UserCreationData
from schemas.auth_data import Token
from utils.jwt_handlers import verify_token

router = APIRouter()

admin_scheme = OAuth2PasswordBearer(tokenUrl="/admin/users")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)

#______________________________________________________________________________
#
# region Liste des utilisateurs (Admin)
#______________________________________________________________________________
@router.get("/admin/users", response_model=List[UserInfoData])
def get_users(
    token : str  = Depends(admin_scheme), 
    db_session: Session = Depends(get_db_session)) -> list[UserInfoData]:

    if not is_valid_token(token, db_session) :
        raise unauthorised_exception
    
    payload = verify_token(token)
    db_admin = get_current_admin(payload, db_session)

    # statement = select(UserInDb)
    # db_users = db_session.exec(statement).all()

    db_users = db_session.query(UserInDb).all()

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

    if not is_valid_token(token, db_session) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_admin = get_current_admin(payload, db_session)

    if creation_data.role not in ["admin", "user"] :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Role does not exist")
    
    db_user = UserInDb(email=creation_data.email)
    db_user.username = creation_data.username
    db_user.password_hash = get_password_hash(creation_data.email)
    db_user.is_active = False
    db_user.role = creation_data.role
    db_session.add(db_user) 
    db_session.commit()
    #db_session.refresh(db_user)

    user_info_data = UserInfoData(
        email = db_user.email, 
        username = db_user.username,
        is_active= db_user.is_active,
        role= db_user.role)     
         
    return user_info_data

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
#from sqlmodel import Session, select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import timedelta

# application imports
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.password_tools import verify_password, get_password_hash
from core.user_role_tools import get_current_user
from db.token_white_list import register_token, is_valid_token, invalidate_token
from db.session_provider import get_db_session
from models.models import UserInDb
from schemas.auth_data import Token, AuthData
from schemas.users_data import UserActivationData
from utils.jwt_handlers import create_access_token, verify_token



router = APIRouter()

#login_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
activation_scheme = OAuth2PasswordBearer(tokenUrl="/auth/activation")
logout_scheme = OAuth2PasswordBearer(tokenUrl="/auth/logout")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)


#______________________________________________________________________________
#
# region Connexion et récupération du token
#______________________________________________________________________________
@router.post("/auth/login", response_model=Token)
def login_for_access_token(
    auth_data: AuthData, 
    db_session: Session = Depends(get_db_session)) -> Token:
    """
    Connexion à l'API 'Prediction Service' et récupération du jeton d'authentification
    """
    login_unauthorised_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Cherche l'utilisateur dans la base de données par son email
    # statement = select(UserInDb).where(UserInDb.email == auth_data.email)
    # db_user = db_session.exec(statement).one_or_none()

    db_user = db_session.query(UserInDb).filter(UserInDb.email == auth_data.email).first()

    # Vérifie si l'utilisateur existe et si le mot de passe est valide
    if not db_user :
        raise login_unauthorised_exception
    
    if not verify_password(auth_data.password, db_user.password_hash):
        from core.password_tools import get_password_hash
        print(f"auth : {auth_data.password}, db : {db_user.password_hash}, test_hash ; {get_password_hash(auth_data.password)}")
        raise login_unauthorised_exception
         
    # Si l'utilisateur existe et que le mot de passe est valide, créer un token d'accès
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    (expired_time, access_token) = create_access_token(
        data={"sub": db_user.email, "id" : db_user.id}, 
        expires_delta=access_token_expires
    )

    register_token(access_token, expired_time, db_session)

    # Retourne le token d'accès et le type de token
    return Token (access_token = access_token, token_type = "bearer")

#______________________________________________________________________________
#
# region Activation du compte et changement du mot de passe
#______________________________________________________________________________
@router.post("/auth/activation")
def activate_account(
    user_data: UserActivationData, 
    token: str = Depends(activation_scheme), 
    db_session: Session = Depends(get_db_session)):
    """
    Activation du compte et changement du mot de passe
    """

    if not is_valid_token(token, db_session) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload, db_session, need_activated_user=False)
    db_user.is_active = True
    db_user.password_hash = get_password_hash(user_data.new_password)
    
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)

    # Retourne un message de confirmation
    return {"msg": "Account activated and password updated successfully."}

#______________________________________________________________________________
#
# region Déconnexion
#______________________________________________________________________________
@router.post("/auth/logout")
def logout(
    token: str = Depends(logout_scheme),
    db_session: Session = Depends(get_db_session)):
    """
    Déconnexion de l'API 'Prediction Service'
    """

    if not is_valid_token(token, db_session) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload, db_session, need_activated_user=False)
    
    invalidate_token(token, db_session)

    return {"msg": "Logged out successfully. Token is invalidated."}



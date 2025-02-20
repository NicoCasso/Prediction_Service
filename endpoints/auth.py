from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from datetime import timedelta
import core.password_management as pm
from schemas.auth_data import Token, AuthData
from schemas.users_data import UserBaseData
from models.models import UserInDb
from utils.jwt_handlers import create_access_token, verify_token, get_current_user
from db.session_provider import get_db_session
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()

#login_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
activation_scheme = OAuth2PasswordBearer(tokenUrl="/auth/activation")
logout_scheme = OAuth2PasswordBearer(tokenUrl="/auth/logout")

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
    unauthorised_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Cherche l'utilisateur dans la base de données par son email
    db_user = db_session.query(UserInDb).filter(UserInDb.email == auth_data.email).first()

    # Vérifie si l'utilisateur existe et si le mot de passe est valide
    if not db_user :
        raise unauthorised_exception
    
    if not pm.verify_password(auth_data.password, db_user.password_hash):
        raise unauthorised_exception
         
    # Si l'utilisateur existe et que le mot de passe est valide, créer un token d'accès
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email, "id" : db_user.id}, 
        expires_delta=access_token_expires
    )

    # Retourne le token d'accès et le type de token
    return Token (access_token = access_token, token_type = "bearer")

#______________________________________________________________________________
#
# region Activation du compte et changement du mot de passe
#______________________________________________________________________________
@router.post("/auth/activation")
def activate_account(
    user_data: UserBaseData, 
    token: str = Depends(activation_scheme), 
    db_session: Session = Depends(get_db_session)):
    """
    Activation du compte et changement du mot de passe
    """
    payload = verify_token(token)
    db_user = get_current_user(payload, db_session)
    
    db_user.password_hash = pm.get_password_hash(user_data.password)
    db_user.is_active = True
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

    payload = verify_token(token)
    db_user = get_current_user(payload)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"msg": "Logged out successfully. Token is invalidated."}



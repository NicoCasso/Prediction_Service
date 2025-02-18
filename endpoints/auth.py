from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from datetime import timedelta
from models import User
from validation_models import UserConnectionData, Token
from dependencies import create_access_token, verify_token, get_current_user
from db_session_provider import get_db_session
from config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()

#______________________________________________________________________________
#
# Connexion et récupération du token
#______________________________________________________________________________
@router.post("/auth/login", response_model=Token)
def login_for_access_token(connection_data: UserConnectionData, 
                           session: Session = Depends(get_db_session)) -> Token:

    # Cherche l'utilisateur dans la base de données par son email
    user = session.query(User).filter(User.email == connection_data.email).first()

    # Vérifie si l'utilisateur existe et si le mot de passe est valide
    if not user or not user.verify_password(connection_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Si l'utilisateur existe et que le mot de passe est valide, créer un token d'accès
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )

    # Retourne le token d'accès et le type de token
    return {"access_token": access_token, "token_type": "bearer"}

#______________________________________________________________________________
#
# Activation du compte et changement du mot de passe
#______________________________________________________________________________
@router.post("/auth/activation")
def activate_account(user: UserConnectionData, 
                     token: str = Depends(verify_token), 
                     session: Session = Depends(get_db_session)):
    
    # Récupère l'utilisateur actuel en fonction du token
    current_user = get_current_user(token)

    # Vérifie si le nom d'utilisateur dans le token correspond à celui fourni dans la requête
    if current_user.email != user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Recherche l'utilisateur dans la base de données par email
    db_user = session.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Mise à jour du mot de passe de l'utilisateur
    db_user.set_password(user.password)  # Met à jour le mot de passe (il est haché)

    # Activer le compte de l'utilisateur
    db_user.is_active = True
    
    # Enregistrer les modifications dans la base de données
    session.commit()
    session.refresh(db_user)

    # Retourne un message de confirmation
    return {"msg": "Account activated and password updated successfully."}


#______________________________________________________________________________
#
# Déconnexion
#______________________________________________________________________________
@router.post("/auth/logout")
def logout(token: str = Depends(verify_token)):
    return {"msg": "Logged out successfully. Token is invalidated."}



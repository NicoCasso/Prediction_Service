from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from ..models import User, UserCreate, Token
from ..dependencies import get_session, create_access_token, verify_token
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

#______________________________________________________________________________
#
# Connexion et récupération du token
#______________________________________________________________________________
@router.post("/auth/login", response_model=Token)
def login_for_access_token(form_data: UserCreate, session: Session = Depends(get_session)) -> Token:
    user = session.query(User).filter(User.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#______________________________________________________________________________
#
# Activation du compte et changement du mot de passe
#______________________________________________________________________________
@router.post("/auth/activation")
def activate_account(user: UserCreate, token: str = Depends(verify_token), session: Session = Depends(get_session)):
    current_user = get_current_user(token)
    if current_user.username != user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    db_user = session.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db_user.set_password(user.password)  # Update password
    session.commit()
    session.refresh(db_user)
    return {"msg": "Account activated and password updated successfully."}

#______________________________________________________________________________
#
# Déconnexion
#______________________________________________________________________________
@router.post("/auth/logout")
def logout(token: str = Depends(verify_token)):
    return {"msg": "Logged out successfully. Token is invalidated."}



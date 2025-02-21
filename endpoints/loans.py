from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
#from sqlmodel import Session, select
from sqlalchemy.orm import Session
from typing import List

# application imports
from core.user_role_tools import get_current_user
from db.session_provider import get_db_session
from db.token_white_list import register_token, is_valid_token, invalidate_token
from models.models import LoanRequestInDb
from schemas.loans_data import LoanRequestData,LoanResponseData, LoanPredictData, LoanInfoData
from utils.jwt_handlers import verify_token


router = APIRouter()

predict_scheme = OAuth2PasswordBearer(tokenUrl="/loans/predict")
request_scheme = OAuth2PasswordBearer(tokenUrl="/loans/request")
history_scheme = OAuth2PasswordBearer(tokenUrl="/loans/history")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)

#______________________________________________________________________________
#
# region Prédiction d'éligibilité à un prêt
#______________________________________________________________________________
@router.get("/loans/predict") #, response_model=LoanPredictData)
def predict_loan_eligibility(
    token: str = Depends(predict_scheme), 
    db_session: Session = Depends(get_db_session) ) : # -> LoanPredictData: 
    """
    Prédiction d'éligibilité à un prêt
    """

    if not is_valid_token(token, db_session) :
        raise unauthorised_exception

    payload = verify_token(token)
    current_user = get_current_user(payload, db_session)

    # Logique de prédiction (ex. basée sur des informations utilisateur dans la base de données)
    eligibility = "Eligible"  # Juste un exemple de retour
    return {"eligibility": eligibility}

#______________________________________________________________________________
#
# region Soumission d'une demande de prêt
#______________________________________________________________________________
@router.post("/loans/request") #, response_model=LoanResponseData)
def request_loan(
    loan_request: LoanRequestData, 
    token: str = Depends(request_scheme), 
    db_session: Session = Depends(get_db_session)) : # -> LoanResponseData:
    """
    Soumission d'une demande de prêt
    """

    if not is_valid_token(token, db_session) :
        raise unauthorised_exception
    
    payload = verify_token(token)
    current_user = get_current_user(payload, db_session)

    new_loan = LoanRequestInDb(user_id=current_user.id, **loan_request)
    db_session.add(new_loan)
    db_session.commit()

    # db_session.refresh(new_loan)
    
    return {"msg": "Loan request submitted successfully."}

#______________________________________________________________________________
#
# region Historique des demandes de prêt
#______________________________________________________________________________
@router.get("/loans/history") #, response_model=List[LoanInfoData])
def loan_history(
    token: str = Depends(history_scheme), 
    db_session: Session = Depends(get_db_session)) : # -> list[LoanInfoData]:
    """
    Historique des demandes de prêt
    """

    if not is_valid_token(token, db_session) :
        raise unauthorised_exception
    
    payload = verify_token(token)
    current_user = get_current_user(payload, db_session)

    # statement = select(LoanRequestInDb).where(LoanRequestInDb.user_id == current_user.id)
    # loan_history = db_session.exec(statement).all()

    loan_history = db_session.query(LoanRequestInDb).filter(LoanRequestInDb.user_id == current_user.id).all()

    return {"loan_history": loan_history}


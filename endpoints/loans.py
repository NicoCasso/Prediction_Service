from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_handlers import verify_token, get_current_user

from sqlalchemy.orm import Session
from models.models import LoanRequestInDb
from db.session_provider import get_db_session


router = APIRouter()

predict_scheme = OAuth2PasswordBearer(tokenUrl="/loans/predict")
request_scheme = OAuth2PasswordBearer(tokenUrl="/loans/request")
history_scheme = OAuth2PasswordBearer(tokenUrl="/loans/history")

#______________________________________________________________________________
#
# region Prédiction d'éligibilité à un prêt
#______________________________________________________________________________
@router.get("/loans/predict")
def predict_loan_eligibility(
    token: str = Depends(predict_scheme), 
    db_session: Session = Depends(get_db_session) ):
    """
    Prédiction d'éligibilité à un prêt
    """
    payload = verify_token(token)
    current_user = get_current_user(token)

    # Logique de prédiction (ex. basée sur des informations utilisateur dans la base de données)
    eligibility = "Eligible"  # Juste un exemple de retour
    return {"eligibility": eligibility}

#______________________________________________________________________________
#
# region Soumission d'une demande de prêt
#______________________________________________________________________________
@router.post("/loans/request")
def request_loan(
    loan_request: dict, 
    token: str = Depends(request_scheme), 
    db_session: Session = Depends(get_db_session)):
    """
    Soumission d'une demande de prêt
    """
    payload = verify_token(token)
    current_user = get_current_user(token)

    new_loan = LoanRequestInDb(user_id=current_user.id, **loan_request)
    db_session.add(new_loan)
    db_session.commit()

    # db_session.refresh(new_loan)
    
    return {"msg": "Loan request submitted successfully."}

#______________________________________________________________________________
#
# region Historique des demandes de prêt
#______________________________________________________________________________
@router.get("/loans/history")
def loan_history(
    token: str = Depends(history_scheme), 
    db_session: Session = Depends(get_db_session)):
    """
    Historique des demandes de prêt
    """
    payload = verify_token(token)
    current_user = get_current_user(payload, db_session)

    loan_history = db_session.query(LoanRequestInDb).filter(LoanRequestInDb.user_id == current_user.id).all()
    return {"loan_history": loan_history}


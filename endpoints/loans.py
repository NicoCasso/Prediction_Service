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
from schemas.loans_data import LoanRequestData, LoanResponseData, LoanInfoData
from utils.jwt_handlers import verify_token
from utils.fake_model import FakeModel


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
# region Soumission d'une demande de prêt
#______________________________________________________________________________
@router.post("/loans/request", response_model=LoanResponseData)
def request_loan(
    loan_request_data: LoanRequestData, 
    token: str = Depends(request_scheme), 
    db_session: Session = Depends(get_db_session)) -> LoanResponseData:
    """
    Soumission d'une demande de prêt
    """
    if not is_valid_token(token, db_session) :
        raise unauthorised_exception
    
    payload = verify_token(token)
    current_user = get_current_user(payload, db_session)

    new_loan = LoanRequestInDb(
        user_id = current_user.id, 
        state = loan_request_data.state,
        bank = loan_request_data.bank,
        naics = loan_request_data.naics,
        term = loan_request_data.term,
        no_emp = loan_request_data.no_emp,
        new_exist = loan_request_data.new_exist,
        create_job = loan_request_data.create_job,
        retained_job = loan_request_data.create_job,
        urban_rural = loan_request_data.urban_rural,
        rev_line_cr= loan_request_data.rev_line_cr,
        low_doc = loan_request_data.low_doc,
        gr_appv = loan_request_data.gr_appv,
        recession = loan_request_data.recession,
        has_franchise = loan_request_data.has_franchise)

    db_session.add(new_loan)
    db_session.commit()
    db_session.refresh(new_loan)

    fake_model = FakeModel(new_loan)
    predicted = fake_model.predict_mis_status()

    new_loan.mis_status = predicted
    db_session.add(new_loan)
    db_session.commit()

    # db_session.refresh(new_loan)

    response_data = LoanResponseData(mis_status=predicted)
    
    return response_data

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


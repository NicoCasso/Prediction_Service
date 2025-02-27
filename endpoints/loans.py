from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from core.user_role_tools import get_current_user
from db.session_provider import get_db_session
from db.token_white_list import register_token, is_valid_token, invalidate_token
from models.models import LoanRequestInDb
from schemas.loans_data import LoanRequestData, LoanResponseData, LoanInfoData
from utils.jwt_handlers import verify_token
from utils.fake_model import FakeModel
from startpoint.max_model import MaxModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Initialize FastAPI app and router
app = FastAPI()
router = APIRouter()
predict_scheme = OAuth2PasswordBearer(tokenUrl="/loans/predict")
request_scheme = OAuth2PasswordBearer(tokenUrl="/loans/request")
history_scheme = OAuth2PasswordBearer(tokenUrl="/loans/history")

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#______________________________________________________________________________
#
# region loan_request
#______________________________________________________________________________
@router.post("/request", response_model=LoanResponseData)
def loan_request(
    loan_request_data: LoanRequestData, 
    token: str = Depends(request_scheme), 
    db_session: Session = Depends(get_db_session)
) -> LoanResponseData:
    """
    Submits a loan request by recording the request data in the database
    and returning the loan approval status.

    Parameters:
    - `loan_request_data` (LoanRequestData): Data of the loan request sent by the user.
      Contains information such as the type of business, the amount of the loan, etc.
    - `token` (str): Token used to authenticate the user making the request.
    """
    logger.debug("Received loan request")
    if not is_valid_token(token, db_session):
        logger.warning("Invalid token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_token(token)
    current_user = get_current_user(payload, db_session)
    logger.debug(f"User ID: {current_user.id}")

    try:
        db_data = LoanRequestInDb(
            user_id=current_user.id,
            state=loan_request_data.state,
            bank=loan_request_data.bank,
            naics=str(loan_request_data.naics),
            term=loan_request_data.term,
            no_emp=loan_request_data.no_emp,
            new_exist=loan_request_data.new_exist,
            create_job=loan_request_data.create_job,
            retained_job=loan_request_data.retained_job,
            urban_rural=loan_request_data.urban_rural,
            rev_line_cr=loan_request_data.rev_line_cr,
            low_doc=loan_request_data.low_doc,
            gr_appv=loan_request_data.gr_appv,
            recession=loan_request_data.recession,
            has_franchise=loan_request_data.has_franchise,
        )
        db_session.add(db_data)
        db_session.commit()
        db_session.refresh(db_data)
        logger.debug(f"Loan request data saved: {db_data}")

        max_model = MaxModel(db_data)
        predicted = max_model.predict_approval_status()
        db_data.approval_status = predicted
        db_session.commit()
        logger.debug(f"Prediction successful: {predicted}")

        return LoanResponseData(approval_status=predicted)
    except Exception as ex:
        db_session.rollback()
        logger.error(f"Error during prediction: {str(ex)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne: {str(ex)}",
        ) from ex

#______________________________________________________________________________
#
# region loan_history
#______________________________________________________________________________
@router.get("/history", response_model=List[LoanInfoData])
def loan_history(
    token: str = Depends(history_scheme), 
    db_session: Session = Depends(get_db_session)
) -> List[LoanInfoData]:
    """
    Retrieves the history of loan requests.

    Parameters:
    - `token` (str): Token used to authenticate the user making the request.
    """
    logger.debug("Received loan history request")
    if not is_valid_token(token, db_session):
        logger.warning("Invalid token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_token(token)
    current_user = get_current_user(payload, db_session)

    try:
        if current_user.role == "admin":
            loan_history = db_session.query(LoanRequestInDb).all()
        else:
            loan_history = db_session.query(LoanRequestInDb).filter(LoanRequestInDb.user_id == current_user.id).all()

        return [LoanInfoData(**loan.model_dump()) for loan in loan_history]
    except Exception as ex:
        logger.error(f"Error fetching loan history: {str(ex)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération de l'historique des prêts"
        )
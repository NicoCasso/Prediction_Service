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
from startpoint.max_model import MaxModel


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
# region loan_request
#______________________________________________________________________________
@router.post("/loans/request", response_model=LoanResponseData)
def loan_request(
    loan_request_data: LoanRequestData, 
    token: str = Depends(request_scheme), 
    db_session: Session = Depends(get_db_session)) -> LoanResponseData:
    """
    Soumet une demande de prêt en enregistrant les informations de la requête
    dans la base de données et en retournant le statut d'approbation du prêt.
    
    Cette méthode prend en entrée les données d'une demande de prêt, vérifie
    l'authenticité du token utilisateur, et effectue une prédiction concernant 
    l'approbation du prêt. Après traitement, elle retourne le statut d'approbation.

    ### Paramètres :
    - `loan_request_data` (LoanRequestData) : Données de la demande de prêt envoyées par l'utilisateur. Contient 
      des informations telles que le type d'entreprise, le montant du prêt, etc.
    - `token` (str) : Token d'authentification utilisé pour vérifier l'utilisateur effectuant la demande. 
    ### Réponse :
    - Retourne un objet `LoanResponseData` avec le statut d'approbation de la demande de prêt.
    
    ### Code d'erreur :
        Erreurs : 401 Unauthorized, 404 Not found
    """
    if not is_valid_token(token, db_session) :
        raise unauthorised_exception
    
    payload = verify_token(token)
    current_user = get_current_user(payload, db_session)

    # new_loan = LoanRequestInDb(
    #     state = "OH",
    #     bank = "CAPITAL ONE NATL ASSOC",
    #     naics = 54, 
    #     term= 60,
    #     no_emp = 13,
    #     new_exist = 1, # =True 
    #     create_job = 0,
    #     retained_job= 3,
    #     urban_rural =2,
    #     rev_line_cr= 0, # = False 
    #     low_doc = 0, # = False 
    #     gr_appv = 50000,
    #     recession = 0, # = False 
    #     has_franchise = 1  # =True 
    # )

    db_data = LoanRequestInDb(
        user_id = current_user.id,
        state = loan_request_data.state, # = str
        bank = loan_request_data.bank, # = str
        naics = loan_request_data.naics, # will be casted in str
        term= loan_request_data.term,
        no_emp = loan_request_data.no_emp,
        new_exist = loan_request_data.new_exist, # = bool 
        create_job = loan_request_data.create_job,
        retained_job= loan_request_data.retained_job,
        urban_rural =loan_request_data.urban_rural,
        rev_line_cr= loan_request_data.rev_line_cr, # = bool 
        low_doc = loan_request_data.low_doc, # = bool 
        gr_appv = loan_request_data.gr_appv, # = float
        recession = loan_request_data.recession, # = bool 
        has_franchise = loan_request_data.has_franchise, # = bool 
    )

    db_session.add(db_data)
    db_session.commit()
    db_session.refresh(db_data)

    #fake_model = FakeModel(new_loan)
    #predicted = fake_model.predict_approval_status()
   
    successful = False
    loan_response_data = None
    try:
        max_model = MaxModel(db_data)
        predicted = max_model.predict_approval_status()
        successful = True
    except Exception as ex :
        loan_response_data = LoanResponseData(approval_status= str(ex) )
        
    if successful :
        db_data.approval_status =  predicted
        db_session.add(db_data)
        db_session.commit()
        loan_response_data = LoanResponseData(approval_status=predicted)
    
    return loan_response_data

#______________________________________________________________________________
#
# region loan_history 
#______________________________________________________________________________
@router.get("/loans/history", response_model=List[LoanInfoData])
def loan_history(
    token: str = Depends(history_scheme), 
    db_session: Session = Depends(get_db_session))  -> list[LoanInfoData]:
    """
    Historique des demandes de prêt
    """

    if not is_valid_token(token, db_session) :
        raise unauthorised_exception
    
    payload = verify_token(token)
    current_user = get_current_user(payload, db_session)

    # statement = select(LoanRequestInDb).where(LoanRequestInDb.user_id == current_user.id)
    # loan_history = db_session.exec(statement).all()

    if current_user.role == "admin" :
        loan_history = db_session.query(LoanRequestInDb).all()
    else :
        loan_history = db_session.query(LoanRequestInDb).filter(LoanRequestInDb.user_id == current_user.id).all()

    return_value = []
    for single_loan in loan_history :
        return_value.append( 
            LoanInfoData(
                user_id = current_user.id, 
                state = single_loan.state,
                bank = single_loan.bank,
                naics = single_loan.naics,
                term = single_loan.term,
                no_emp = single_loan.no_emp,
                new_exist = single_loan.new_exist,
                create_job = single_loan.create_job,
                retained_job = single_loan.create_job,
                urban_rural = single_loan.urban_rural,
                rev_line_cr= single_loan.rev_line_cr,
                low_doc = single_loan.low_doc,
                gr_appv = single_loan.gr_appv,
                recession = single_loan.recession,
                has_franchise = single_loan.has_franchise, 
                approval_status=single_loan.approval_status)
        )

    loan_list : list[LoanInfoData] = return_value

    return loan_list


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from alembic.models.endpoints.user import LoanRequest
from db_session_provider import get_db_session
from dependencies import verify_token, get_current_user
from Schemas import Loanpredict
import pickle

router = APIRouter()

#______________________________________________________________________________
#
# region Prédiction d'éligibilité à un prêt
#______________________________________________________________________________
# @router.get("/loans/predict")
# def predict_loan_eligibility(token: str = Depends(verify_token)):
#     current_user = get_current_user(token)
#     # Logique de prédiction (ex. basée sur des informations utilisateur dans la base de données)
#     eligibility = "Eligible"  # Juste un exemple de retour
#     return {"eligibility": eligibility}

@router.get("/loans/predict")
def predict_loan_eligibility(data: Loanpredict):

    with open("endpoints/cat_boost_model.pkl", "rb") as f:
        model = pickle.load(f)
    
    features = [
        [data.State,
         data.Bank,
        data.NAICS,
        data.Term,
        data.NoEmp,
        data.NewExist,
        data.CreateJob,
        data.RetainedJob,
        data.UrbanRural,
        data.RevLineCr,
        data.LowDoc,
        data.GrAppv,
        data.Recession,
        data.HasFranchise]
    ]

    resultat = model.predict(features)

    return{ "prediction" : resultat[0]}


#______________________________________________________________________________
#
# region Soumission d'une demande de prêt
#______________________________________________________________________________
@router.post("/loans/request")
def request_loan(loan_request: dict, token: str = Depends(verify_token), session: Session = Depends(get_db_session)):
    current_user = get_current_user(token)
    new_loan = LoanRequest(user_id=current_user.id, **loan_request)
    session.add(new_loan)
    session.commit()
    session.refresh(new_loan)
    return {"msg": "Loan request submitted successfully."}

#______________________________________________________________________________
#
# region Historique des demandes
#______________________________________________________________________________
@router.get("/loans/history")
def loan_history(token: str = Depends(verify_token), session: Session = Depends(get_db_session)):
    current_user = get_current_user(token)
    loan_history = session.query(LoanRequest).filter(LoanRequest.user_id == current_user.id).all()
    return {"loan_history": loan_history}


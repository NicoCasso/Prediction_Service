from pydantic import BaseModel
#______________________________________________________________________________
#
# region Loan request Data
#______________________________________________________________________________
class LoanRequestData(BaseModel):
    amount: int
    term : int

#______________________________________________________________________________
#
# region Loan response Data
#______________________________________________________________________________
class LoanResponseData(BaseModel):
    amount: int
    prediction : str

#______________________________________________________________________________
#
# region Loan predict Data
#______________________________________________________________________________
class LoanPredictData(BaseModel):
    amount: int
    something : str

#______________________________________________________________________________
#
# region Loan info Data
#______________________________________________________________________________
class LoanInfoData(BaseModel):
    amount: int
    term : int
    something : str
    prediction : str

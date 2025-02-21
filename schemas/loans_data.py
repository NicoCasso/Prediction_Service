from pydantic import BaseModel
#______________________________________________________________________________
#
# region Loan request Data
#______________________________________________________________________________
class LoanRequestData(BaseModel):
    state : str
    bank : str
    naics : int
    term : int 
    no_emp : int 
    new_exist : bool 
    create_job : int 
    retained_job: int 
    urban_rural: int 
    rev_line_cr: bool 
    low_doc : bool 
    gr_appv: int 
    recession: bool 
    has_franchise: bool 

#______________________________________________________________________________
#
# region Loan response Data
#______________________________________________________________________________
class LoanResponseData(BaseModel):
    mis_status : str

#______________________________________________________________________________
#
# region Loan info Data
#______________________________________________________________________________
class LoanInfoData(LoanRequestData):
    mis_status : str

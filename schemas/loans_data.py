from pydantic import BaseModel, Field
from typing import Optional
#______________________________________________________________________________
#
# region Loan request Data
#______________________________________________________________________________
class LoanRequestData(BaseModel):
    """
    data used for loan prediction
    """
    state : str = Field(description = "State, encoded on 2 characters")
    bank : str = Field(description = "Bank name")
    naics : int = Field(description = "North American industry classiﬁcation system code, \n first two characters")
    term : int = Field(description = "Loan term in months")
    no_emp : int = Field(description = "Number of business employees")
    new_exist : Optional[int] = Field(description = "1 = Existing business, 2 = New business")
    create_job : int = Field(description = "number of jobs created")
    retained_job: int = Field(description = "number of jobs saved")
    urban_rural: int = Field(description = "1 = Urban, 2 = rural, 0 = undeﬁned")
    rev_line_cr: Optional[int] = Field(description = "Revolving line of credit: 1 = Yes, 0 = No")
    low_doc : Optional[int] = Field(description = "LowDoc Loan Program: 1 = Yes, 0 = No")
    gr_appv: int = Field(description = "Gross amount of loan approved by bank")
    recession: Optional[int] = Field(description = "From December 2007 to June 2009")
    has_franchise: Optional[int] = Field(description = "has a franchise code or not")

#______________________________________________________________________________
#
# region Loan response Data
#______________________________________________________________________________
class LoanResponseData(BaseModel):
    approval_status : str

#______________________________________________________________________________
#
# region Loan info Data
#______________________________________________________________________________
class LoanInfoData(LoanRequestData):
    approval_status : str

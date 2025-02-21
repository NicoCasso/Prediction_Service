from pydantic import BaseModel, EmailStr
from typing import Optional

class Loanpredict(BaseModel):
    State : str
    Bank : str
    NAICS : int
    Term : int
    NoEmp : int
    NewExist : int
    CreateJob : int
    RetainedJob: int
    UrbanRural: int
    RevLineCr: int
    LowDoc: int
    GrAppv: int
    Recession: int
    HasFranchise: int


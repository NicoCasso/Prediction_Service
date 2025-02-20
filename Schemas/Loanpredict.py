from pydantic import BaseModel, EmailStr
from typing import Optional

class Loanpredict(BaseModel):
    State : str
    Bank : str
    NAICS : int
    Term : int
    NoEmp : int
    NewExist : bool
    CreateJob : int
    RetainedJob: int
    UrbanRural: int
    RevLineCr: bool
    LowDoc: bool
    GrAppv: int
    Recession: bool
    HasFranchise: bool


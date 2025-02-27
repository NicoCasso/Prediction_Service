from pydantic import BaseModel
from typing import Optional

#______________________________________________________________________________
#
# region User activation Data
#______________________________________________________________________________
class UserActivationData(BaseModel):
    """
    User activation Data
    """
    new_password : str

#______________________________________________________________________________
#
# region User information data
#______________________________________________________________________________
class UserInfoData(BaseModel):
    """
    User information data 
    """
    email: str
    username : Optional [str] = None
    is_active : bool
    role: str = "user"

#______________________________________________________________________________
#
# region Creation data needed for a User 
#______________________________________________________________________________
class UserCreationData(BaseModel):
    """
    All data excluding 'is_active' field
    """
    email: str
    username : Optional [str] = None
    role: str = "user"
    password : str




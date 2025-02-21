from pydantic import BaseModel, EmailStr
from typing import Optional

#______________________________________________________________________________
#
# region User activation Data
#______________________________________________________________________________
class UserActivationData(BaseModel):
    """
    User activation Data
    """
    email: EmailStr
    is_active : bool
    new_password : str

#______________________________________________________________________________
#
# region User information data
#______________________________________________________________________________
class UserInfoData(BaseModel):
    """
    User information data 
    """
    email: EmailStr
    username : Optional [str] = None
    is_active : bool
    role: str = "user"

#______________________________________________________________________________
#
# region All data from User 
#______________________________________________________________________________
class UserCreationData(UserInfoData):
    """
    All data
    """
    password : str




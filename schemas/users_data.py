from pydantic import BaseModel, EmailStr, Field
from typing import Optional

#______________________________________________________________________________
#
# region User connexion data
#______________________________________________________________________________
class UserConnectData(BaseModel):
    email: str
    password: str

#______________________________________________________________________________
#
# region User activation Data
#______________________________________________________________________________
class UserBaseData(BaseModel):
    email: str
    is_active : bool

#______________________________________________________________________________
#
# region User information data
#______________________________________________________________________________
class UserInfoData(UserBaseData):
    username : Optional [str] = None
    role: str = "user"

#______________________________________________________________________________
#
# region All data from User 
#______________________________________________________________________________
class UserCreationData(UserInfoData):
    password : str




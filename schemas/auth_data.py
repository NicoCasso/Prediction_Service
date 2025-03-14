from pydantic import BaseModel

#______________________________________________________________________________
#
# region AuthData données utilisées pour le login 
#______________________________________________________________________________
class AuthData(BaseModel):
    email:str
    password:str

#______________________________________________________________________________
#
# region JWT Web Token
#______________________________________________________________________________
class Token(BaseModel):
    access_token: str  # Le token d'accès généré
    token_type: str    # Le type du token, généralement "bearer"




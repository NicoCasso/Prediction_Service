from pydantic import BaseModel, EmailStr, Field
from typing import Optional

#______________________________________________________________________________
#
# region Champ utilisé pour le JWT Web Token
#______________________________________________________________________________
class Token(BaseModel):
    access_token: str  # Le token d'accès généré
    token_type: str    # Le type du token, généralement "bearer"

#______________________________________________________________________________
#
# region Validateur des données de connexion
#______________________________________________________________________________
class UserConnectionData(BaseModel):
    email: str
    password: str

    class Config:
        from_attribute = True

#______________________________________________________________________________
#
# region Validateur des données utilisateur
#______________________________________________________________________________
class UserCreationData(BaseModel):
    email: EmailStr = Field(..., unique=True, index=True, nullable=False)
    password: str = Field(..., min_length=6)  # Le mot de passe doit avoir au moins 6 caractères
    role: Optional[str] = Field(default="user", alias="role")  # Le rôle par défaut est "user"
    is_active: Optional[bool] = Field(default=False)  # Le compte est désactivé par défaut

    class Config:
        from_attribute = True  # Cela permet de convertir le modèle Pydantic en un modèle SQLAlchemy si besoin

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from passlib.context import CryptContext
from typing import List, Optional

#______________________________________________________________________________
#
# region UserInDB : l'objet User tel qu'il est stocké dans la base de données
#______________________________________________________________________________
class UserInDb(SQLModel, table=True):
    """
        id: Identifiant unique de l'utilisateur.
        username .. ajouté
        email: L'email unique de l'utilisateur.
        password_hash: Le mot de passe haché.
        role: Le rôle de l'utilisateur (par exemple, "user" ou "admin").
        is_active: Un champ booléen pour savoir si le compte est activé ou non.
        loans: Une relation avec la table LoanRequest, 
        chaque utilisateur peut avoir plusieurs demandes de prêt.
        """
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    username : str = Field(default="Vous", nullable=True)
    email: str = Field(unique=True, index=True, nullable=False)
    password_hash: str
    role: str = Field(default="user", nullable=False)
    is_active: bool = Field(default=False)
    
    # Relation pour lier les demandes de prêt à un utilisateur
    loans: List["LoanRequestInDb"] = Relationship(back_populates="user")



#______________________________________________________________________________
#
# region LoanRequestInDb : l'objet LoanRequest tel qu'il est stocké dans la base de données
#______________________________________________________________________________
class LoanRequestInDb(SQLModel, table=True):
    __tablename__ = "loan_requests"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")

    # request fields
    state : str = Field()
    bank : str = Field()
    naics : int = Field()
    term : int = Field()
    no_emp : int = Field()
    new_exist : bool = Field()
    create_job : int = Field()
    retained_job: int = Field()
    urban_rural: int = Field()
    rev_line_cr: bool = Field()
    low_doc : bool = Field()
    gr_appv: int = Field()
    recession: bool = Field()
    has_franchise: bool = Field()
    
    #request status
    approval_status: Optional[str] = Field(default=None)

    # Relation pour lier une demande de prêt à un utilisateur
    user: UserInDb = Relationship(back_populates="loans")
    
#______________________________________________________________________________
#
# region TokenInDB : white list de token valides
#______________________________________________________________________________
class TokenInDB(SQLModel, table=True):
    __tablename__ = "valid_tokens"
    id: int = Field(default=None, primary_key=True)
    expires : datetime = Field()
    token : str = Field()
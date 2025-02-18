from sqlmodel import Field, SQLModel, Relationship
from passlib.context import CryptContext
from typing import List, Optional


class User(SQLModel, table=True):
    """
    id: Identifiant unique de l'utilisateur.
        email: L'email unique de l'utilisateur.
        password_hash: Le mot de passe haché.
        role: Le rôle de l'utilisateur (par exemple, "user" ou "admin").
        is_active: Un champ booléen pour savoir si le compte est activé ou non.
        loans: Une relation avec la table LoanRequest, 
        chaque utilisateur peut avoir plusieurs demandes de prêt."""
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    password_hash: str
    role: str = Field(default="user", nullable=False)
    is_active: bool = Field(default=False)
    
    # Relation pour lier les demandes de prêt à un utilisateur
    loans: List["LoanRequest"] = Relationship(back_populates="user")

    def set_password(self, password: str):
        """
        set_password: Utilise passlib pour hacher le mot de passe avant de le stocker.
        """
        self.password_hash = CryptContext(schemes=["bcrypt"]).hash(password)

    def verify_password(self, password: str) -> bool:
        """
        Vérifie si le mot de passe fourni correspond à celui stocké dans la base de données.
        """
        return CryptContext(schemes=["bcrypt"]).verify(password, self.password_hash)


class LoanRequest(SQLModel, table=True):
    __tablename__ = "loan_requests"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    amount: float = Field(..., nullable=False)
    status: str = Field(default="pending", nullable=False)

    # Relation pour lier une demande de prêt à un utilisateur
    user: User = Relationship(back_populates="loans")

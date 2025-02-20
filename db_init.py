from sqlmodel import SQLModel, create_engine
from alembic.models.endpoints.user import User, LoanRequest
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

# Créer les tables
SQLModel.metadata.create_all(engine)

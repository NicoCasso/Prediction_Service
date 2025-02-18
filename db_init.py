from sqlmodel import SQLModel, create_engine
from models import User, LoanRequest

# Configurer la base de données (exemple avec SQLite en mémoire)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)

# Créer les tables
SQLModel.metadata.create_all(engine)

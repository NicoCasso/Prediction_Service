from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, Session
from core.config import DATABASE_URL

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # connect_args nécessaire pour SQLite

# SessionMaker pour gérer les sessions SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Définition de la base
Base : DeclarativeMeta = declarative_base()

# Fonction pour obtenir une session DB
def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

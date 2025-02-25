from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, DeclarativeMeta, sessionmaker, Session 
from typing import Generator, Any

#application imports
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # connect_args nécessaire pour SQLite

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base: DeclarativeMeta = declarative_base()

def get_db_session() -> Generator[Session, Any, None]:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

        
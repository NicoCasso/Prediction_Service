from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from contextlib import contextmanager

#application imports
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # connect_args nécessaire pour SQLite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session_scope = scoped_session(SessionLocal)

Base: DeclarativeMeta = declarative_base()

@contextmanager
def get_db_session() -> Session:
    db_session = session_scope()  
    try:
        yield db_session
    finally:
        db_session.remove()
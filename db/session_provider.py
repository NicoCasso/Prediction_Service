from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, DeclarativeMeta, sessionmaker, Session 
from typing import Generator, Any

#application imports
from core.config import CONNECTION_STRING, CONNECTION_ARGS

conn_args = CONNECTION_ARGS
#conn_args["check_same_thread"] = False nécessaire pour sqlite

engine = create_engine(CONNECTION_STRING, connect_args=conn_args)  

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base: DeclarativeMeta = declarative_base()

def get_db_session() -> Generator[Session, Any, None]:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

        
from sqlmodel import SQLModel, create_engine
from core.config import CONNECTION_STRING, CONNECTION_ARGS

engine = create_engine(CONNECTION_STRING, connect_args=CONNECTION_ARGS, echo=True)

def initialise_database():
    SQLModel.metadata.create_all(engine)







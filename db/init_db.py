from sqlmodel import SQLModel, create_engine
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

def initialise_database():
    SQLModel.metadata.create_all(engine)







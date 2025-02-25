from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, DeclarativeMeta, sessionmaker, Session 

#application imports
from core.config import DATABASE_URL
from models.models import UserInDb
from schemas.users_data import UserCreationData

from core.password_tools import get_password_hash

from main import app

object_list = []
object_list.append(
    UserCreationData(
        email="nicolas.cassonnet@wanadoo.fr",
        username = "Nicolas",
        password = "nicolas.cassonnet@wanadoo.fr", 
        role = "admin")
)
object_list.append(
    UserCreationData( 
        email="user1.fakemail@fakeprovider.com",
        username = "User1",
        password = "initialpass1", 
        role = "user")
)
object_list.append(
    UserCreationData( 
        email="user2.fakemail@fakeprovider.com",
        username = "User2",
        password = "initialpass2", 
        role = "user")
)

# code equivalent à :
#   from typing import cast 
#   users_list = cast(list[UserData], object_list)
original_users_list : list[UserCreationData] = object_list

def populate_with_users(users_data : list[UserCreationData]) :

    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # connect_args nécessaire pour SQLite
    SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    Base: DeclarativeMeta = declarative_base()
    
    try:
        # Ouvrir une session
        db_session = SessionLocal()
    
        for user_data in users_data :

            # statement = select(UserInDb).where(UserInDb.email==user_data.email)
            # result = db_session.exec(statement).one_or_none()

            result = db_session.query(UserInDb).filter(UserInDb.email==user_data.email).first()

            if not result :
                new_user= UserInDb(email=user_data.email)
                new_user.username = user_data.username
                new_user.password_hash = get_password_hash(user_data.password) 
                new_user.role = user_data.role
                new_user.is_active = (user_data.role == "admin")
                db_session.add(new_user)
                db_session.commit()
    finally:
        db_session.close()

    print("done")

if __name__ == "__main__" :
    populate_with_users(original_users_list)

    
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, DeclarativeMeta, sessionmaker, Session 

#application imports
from core.config import CONNECTION_STRING, CONNECTION_ARGS
from models.models import UserInDb
from schemas.users_data import UserCreationData

from core.password_tools import get_password_hash

from main import app

def get_old_password(username : str) :
    number = int(username.replace("User",""))
    old_password = "initialpass"+ str(number)
    return old_password

def get_new_password(username : str) :
    number = int(username.replace("User",""))
    new_password = "otherpass"+ str(number)
    return new_password

object_dict = {}
object_dict["admin"] = UserCreationData(
    email="nicolas.cassonnet@wanadoo.fr",
    username = "Nicolas",
    password = "nicolas.cassonnet@wanadoo.fr", 
    role = "admin")

object_dict["active_user"] = UserCreationData( 
    email="user1.fakemail@fakeprovider.com",
    username = "User1",
    password = get_new_password("User1"), 
    role = "user")

object_dict["inactive_user"] = UserCreationData( 
    email="user2.fakemail@fakeprovider.com",
    username = "User2",
    password = get_old_password("User2"), 
    role = "user")



# code equivalent à :
#   from typing import cast 
#   users_list = cast(list[UserData], object_list)
original_users_dict : dict[str, UserCreationData] = object_dict

def populate_with_users(users_data : dict[str, UserCreationData]) :

    conn_args = CONNECTION_ARGS
    #conn_args["check_same_thread"] = False nécessaire pour sqlite

    engine = create_engine(CONNECTION_STRING, connect_args=conn_args)  
    SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    Base: DeclarativeMeta = declarative_base()
    
    try:
        # Ouvrir une session
        db_session = SessionLocal()
    
        for user_key, user_data in users_data.items() :

            # statement = select(UserInDb).where(UserInDb.email==user_data.email)
            # result = db_session.exec(statement).one_or_none()

            result = db_session.query(UserInDb).filter(UserInDb.email==user_data.email).first()

            if not result :
                new_user= UserInDb(email=user_data.email)
                new_user.username = user_data.username
                new_user.role = user_data.role
                match (user_key) : 
                    case "admin" :
                        new_user.password_hash = get_password_hash(user_data.password) 
                        new_user.is_active = True
                    case "active_user" :
                        new_user.password_hash = get_password_hash(get_new_password(user_data.username)) 
                        new_user.is_active = True
                    case "inactive_user" :
                        new_user.password_hash = get_password_hash(get_old_password(user_data.username)) 
                        new_user.is_active = False

                db_session.add(new_user)
                db_session.commit()
    finally:
        db_session.close()

    print("done")

if __name__ == "__main__" :
    populate_with_users(original_users_dict)

    
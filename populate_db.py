from sqlmodel import SQLModel, Field, Session, create_engine, select
from core.config import DATABASE_URL
from models.models import UserInDb
from schemas.users_data import UserCreationData
from core.password_tools import get_password_hash

object_list = []
object_list.append(
    UserCreationData(
        email="nicolas.cassonnet@wanadoo.fr",
        username = "Nicolas",
        password = "nicolas.cassonnet@wanadoo.fr", 
        role = "admin",
        is_active= True)
)
object_list.append(
    UserCreationData( 
        email="user1.fakemail@fakeprovider.com",
        username = "User1",
        password = "initialpass1", 
        role = "user",
        is_active= False)
)
object_list.append(
    UserCreationData( 
        email="user2.fakemail@fakeprovider.com",
        username = "User2",
        password = "initialpass2", 
        role = "user",
        is_active= False)
)

# code equivalent à :
#   from typing import cast 
#   users_list = cast(list[UserData], object_list)
users_list : list[UserCreationData] = object_list

def populate_with_users(users_data : list[UserCreationData]) :

    engine = create_engine(DATABASE_URL)

    # Ouvrir une session
    with Session(engine) as session:
        # Sélection de chaque utilisateur à ajouter
        
        for user_data in users_data :
            statement = select(UserInDb).where(UserInDb.email==user_data.email)
            result = session.exec(statement).one_or_none()
            if not result :
                new_user= UserInDb(email=user_data.email)
                new_user.username = user_data.username
                new_user.password_hash = get_password_hash(user_data.password)
                new_user.role = user_data.role
                new_user.is_active = user_data.is_active
                session.add(new_user)
                session.commit()

    print("done")

if __name__ == "__main__" :
    populate_with_users(users_list)

    
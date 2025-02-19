from sqlmodel import SQLModel, Field, Session, create_engine, select
from config import DATABASE_URL
from models import User



users = []
users.append({ 
    "username" : "Nicolas",
    "email" : "nicolas.cassonnet@wanadoo.fr",
    "is_active" : True, 
    "password" : "nicolas.cassonnet@wanadoo.fr",
    "role"  : "admin",
})
users.append({ 
    "username" : "User1",
    "email" : "user1.fakemail@fakeprovider.com",
    "is_active" : False, 
    "password" : "initialpass1",
    "role"  : "user"
})
users.append({
    "username" : "User2",
    "email" : "user2.fakemail@fakeprovider.com",
    "is_active" : False, 
    "password" : "initialpass2",
    "role"  : "user"
})

def init() :

    engine = create_engine(DATABASE_URL)

    # Ouvrir une session
    with Session(engine) as session:
        # Sélection de chaque utilisateur à ajouter

        for user in users :
            statement = select(User).where(User.username==user["username"])
            result = session.exec(statement).one_or_none()
            if not result :
                new_user= User(email=user["email"])
                new_user.username = username=user["username"]
                new_user.set_password(user["password"])
                new_user.role = user["role"]
                new_user.is_active = user["is_active"]
                session.add(new_user)
                session.commit()

    print("done")

if __name__ == "__main__" :
    init()

    
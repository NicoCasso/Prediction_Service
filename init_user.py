from sqlmodel import SQLModel, Field, Session, create_engine, select
from config import DATABASE_URL
from models import User


user_email = "nicolas.cassonnet@wanadoo.fr"
user_password = "nicolas.cassonnet@wanadoo.fr"
user_name = "Nicolas"
def init() :

    engine = create_engine(DATABASE_URL)

    # Ouvrir une session
    with Session(engine) as session:
        # Sélection de tous les utilisateurs
        statement = select(User).where(User.email==user_email)
        result = session.exec(statement).one_or_none()
        if not result :
            new_user= User(email=user_email)
            new_user.set_password(user_password)
            new_user.username = user_name
            session.add(new_user)
            session.commit()

    print("done")

if __name__ == "__main__" :
    init()

    
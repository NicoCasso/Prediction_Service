import os
from dotenv import load_dotenv

DATABASE_URL = "sqlite:///./db/prediction_service_db.db" # also present in alembic.ini, section [alembic]
DATABASE_NAME = "prediction_service_db.db"

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "thequickbrownfoxjumpsoverthelazydog")

#SALT = "todayisnotthesamedaythanyesterday"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expiration du token après 30 minutes


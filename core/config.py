import os
from dotenv import load_dotenv


DB_USER = "fastapifirst"
DB_PASSWORD = "passwordfirst1."
DB_HOST = "localhost"
DB_PORT = "1433"
DB_NAME = "prediction_service_db"
DB_DRIVER = "ODBC+Driver+18+for+SQL+Server"

DB_ENCRYPT = "yes"
DB_TRUSTSERVERCERTIFICATE = "yes"

# also present in alembic.ini, section [alembic] 
# sqlalchemy.url=mssql+pyodbc://fastapifirst:passwordfirst1.@localhost:1433/prediction_service_db?driver=ODBC+Driver+18+for+SQL+Server 
CONNECTION_STRING = (
    f"mssql+pyodbc://{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
    f"?driver={DB_DRIVER}"
)

CONNECTION_ARGS = {
    'Encrypt': DB_ENCRYPT,  
    'TrustServerCertificate': DB_TRUSTSERVERCERTIFICATE 
}

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "thequickbrownfoxjumpsoverthelazydog")

#SALT = "todayisnotthesamedaythanyesterday"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expiration du token après 30 minutes


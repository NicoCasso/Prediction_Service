import os
from dotenv import load_dotenv


SECRET_KEY: str = os.getenv("SECRET_KEY", "thequickbrownfoxjumpsoverthelazydog")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

API_CLIENT_ADDRESS = "0.0.0.0"
API_CLIENT_PORT = "8000" #unused ???
API_INTERNAL_PORT = "3100" 

# added by Jeremy manually - pushed here for memory
AZURE_DNS_LABEL= "nicocassoregistry.azurecr.io/prediction-service-image"
AZURE_DNS_PORT = "3100"

DB_USER = "fastapifirst"
DB_PASSWORD = "passwordfirst1."
DB_HOST= "ncassonnetsqlserver.database.windows.net"
#DB_HOST = "localhost"
DB_PORT = "1433"
DB_NAME = "prediction_service_db"
DB_DRIVER = "ODBC+Driver+18+for+SQL+Server"

DB_ENCRYPT = "yes"
DB_TRUSTSERVERCERTIFICATE = "no"
#DB_TRUSTSERVERCERTIFICATE = "yes"
DB_CONNECTION_TIMEOUT = "30"

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
    'TrustServerCertificate': DB_TRUSTSERVERCERTIFICATE,
    'Connection Timeout' : DB_CONNECTION_TIMEOUT
}

# chaine de connection proposée par AZURE :
# _____________________________________________________________________________
#|
#| Driver={ODBC Driver 18 for SQL Server};
#| Server=tcp:ncassonnetsqlserver.database.windows.net,1433;
#| Database=prediction_service_db;
#| Uid=admin_name;
#| Pwd=admin_password;
#| Encrypt=yes;
#| TrustServerCertificate=no;
#| Connection Timeout=30;
#|_____________________________________________________________________________

# Ce que propose ChatGpt : (en enlevant le tcp:)
# "mssql+pyodbc://admin_name:admin_password
# @ncassonnetsqlserver.database.windows.net:1433
# /prediction_service_db
# ?driver=ODBC+Driver+18+for+SQL+Server
# &Encrypt=yes
# &TrustServerCertificate=no
# &Connection Timeout=30"

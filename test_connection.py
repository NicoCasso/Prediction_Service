from db.session_provider import get_db_session
from sqlalchemy import text
import core.config

# Test de connexion
conn_string = (
    f"mssql+pyodbc://{core.config.DB_USER}:"
    f"{core.config.DB_PASSWORD}@"
    f"{core.config.DB_HOST}:"
    f"{core.config.DB_PORT}/"
    f"{core.config.DB_NAME}"
    f"?driver={core.config.DB_DRIVER}"
)

conn_args = {
    'Encrypt': core.config.DB_ENCRYPT,  # Activer le chiffrement
    'TrustServerCertificate': core.config.DB_TRUSTSERVERCERTIFICATE,  # Ignorer les erreurs de certificat SSL
    'Connection Timeout' : core.config.DB_CONNECTION_TIMEOUT # proposed by Azure in the connection string
}

connection_ok = False
try :
    session = next(get_db_session())
    result = session.execute(text("SELECT CURRENT_USER")).fetchone()

    print()
    # Afficher le résultat
    print(f"CURRENT_USER = {result[0]}")  # Affiche le nom de l'utilisateur actuel
    connection_ok = True
except Exception  as e :
    print()
    print(f"ERROR => {e}")
    print()
finally :
    session.close()

if connection_ok :
    print("               _______________________")
    print("              |                       |")
    print("              |  Connexion réussie!   |")
    print("              |_______________________|")
    print()


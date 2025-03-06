from sqlalchemy import create_engine


username = 'fastapifirst'
password = 'passwordfirst1.'

server = 'localhost'
sql_server_port = "1433"
database = 'prediction_service_db'
driver = "ODBC+Driver+18+for+SQL+Server"

encrypt = 'yes'
trust_server_certificate = 'yes'

# Test de connexion
conn_string = (
    f"mssql+pyodbc://{username}:"
    f"{password}@"
    f"{server}:"
    f"{sql_server_port}/"
    f"{database}"
    f"?driver={driver}"
)

conn_args = {
    'Encrypt': encrypt,  # Activer le chiffrement
    'TrustServerCertificate': trust_server_certificate,  # Ignorer les erreurs de certificat SSL
}

engine = create_engine(conn_string, connect_args = conn_args)

# Test de connexion
connection = engine.connect()
print("               _______________________")
print("              |                       |")
print("              |  Connexion réussie!   |")
print("              |_______________________|")
print()
connection.close()

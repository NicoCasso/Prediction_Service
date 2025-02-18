DATABASE_URL = "sqlite:///./prediction_service_db.db" # also present in alembic.ini, section [alembic]
DATABASE_NAME = "prediction_service_db.db"

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expiration du token après 30 minutes
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
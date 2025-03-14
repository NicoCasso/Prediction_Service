# core/config.py (final version)
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "thequickbrownfoxjumpsoverthelazydog")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # Directly use DATABASE_URL from environment
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db/prediction_service_database.db")

    class Config:
        env_file = ".env"

settings = Settings()

# Export the settings instance
DATABASE_URL = settings.DATABASE_URL
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

__all__ = [
    'DATABASE_URL',
    'SECRET_KEY',
    'ALGORITHM',
    'ACCESS_TOKEN_EXPIRE_MINUTES'
]

# import os
# from dotenv import load_dotenv
# from pydantic_settings import BaseSettings  # Updated import
# from typing import Dict

# class Settings(BaseSettings):
#     SECRET_KEY: str = os.getenv("SECRET_KEY", "thequickbrownfoxjumpsoverthelazydog")
#     ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Expiration du token après 30 minutes

#     # Database configuration
#     DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db/prediction_service_database.db")
#     DATABASE_NAME: str = os.getenv("DATABASE_NAME", "prediction_service_database.db")

#     # PostgreSQL configuration
#     POSTGRES_USER: str = os.getenv("POSTGRES_USER", None)
#     POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", None)
#     POSTGRES_DB: str = os.getenv("POSTGRES_DB", None)
#     POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", None)
#     POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", None)
#     POSTGRES_RDY: int = int(os.getenv("POSTGRES_RDY", 0))

#     class Config:
#         env_file = ".env"

# settings = Settings()

# # Load environment variables from .env file
# load_dotenv()

# # Print debugging information
# print("POSTGRES_USER:", settings.POSTGRES_USER)
# print("POSTGRES_PASSWORD:", settings.POSTGRES_PASSWORD)
# print("POSTGRES_DB:", settings.POSTGRES_DB)
# print("POSTGRES_HOST:", settings.POSTGRES_HOST)
# print("POSTGRES_PORT:", settings.POSTGRES_PORT)
# print("POSTGRES_RDY:", settings.POSTGRES_RDY)
# print("SECRET_KEY:", settings.SECRET_KEY)
# print("ALGORITHM:", settings.ALGORITHM)
# print("ACCESS_TOKEN_EXPIRE_MINUTES:", settings.ACCESS_TOKEN_EXPIRE_MINUTES)

# # Determine the database configuration
# if settings.POSTGRES_USER and settings.POSTGRES_PASSWORD and settings.POSTGRES_DB and settings.POSTGRES_HOST and settings.POSTGRES_PORT and settings.POSTGRES_RDY:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': settings.POSTGRES_DB,
#             'USER': settings.POSTGRES_USER,
#             'PASSWORD': settings.POSTGRES_PASSWORD,
#             'HOST': settings.POSTGRES_HOST,
#             'PORT': settings.POSTGRES_PORT,
#         }
#     }
#     print("Using PostgreSQL Database:", DATABASES)
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'prediction_service_database.db'),
#         }
#     }
#     print("Using SQLite Database:", DATABASES)

# # Print the final database configuration for debugging
# print("Final DATABASES:", DATABASES)

# # Export the settings instance
# DATABASE_URL = settings.DATABASE_URL
# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# # Export all variables as global variables
# __all__ = [
#     'DATABASE_URL',
#     'SECRET_KEY',
#     'ALGORITHM',
#     'ACCESS_TOKEN_EXPIRE_MINUTES'
# ]
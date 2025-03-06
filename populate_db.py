from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re
from sqlalchemy.exc import IntegrityError
import logging

# Application imports
from core.config import DATABASE_URL
from models.models import UserInDb
from schemas.users_data import UserCreationData
from core.password_tools import get_password_hash

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper functions for password generation
def get_old_password(username: str) -> str:
    number = int(username.replace("User", ""))
    return f"initialpass{number}"

def get_new_password(username: str) -> str:
    number = int(username.replace("User", ""))
    return f"otherpass{number}"

# Function to check if a password is already hashed
def is_already_hashed(password: str) -> bool:
    """
    Check if the password is already hashed (starts with $2b$).
    """
    return re.match(r"^\$2[abxy]\$\d{2}\$", password) is not None

# Predefined user data
object_dict = {
    "admin_max": UserCreationData(
        email="max.fla@simplon.fr",
        username="Max",
        password="maxfla",
        role="admin",
    ),
    # "active_user": UserCreationData(
    #     email="usermike@test.com",
    #     username="usermike",
    #     password="$2b$12$4Ycft6eU9X5rWXlR4LrsHO2kXZ7B/3pu6P/WKEJJt6Z5kfbt.dx6W",
    #     role="user",
    # ),
    # "admin_mike": UserCreationData(
    #     email="mike@test.com",
    #     username="adminmike",
    #     password="$2b$12$rIOqGQhPBhksARaOz.qHz.rm4tHqmA2DUtMNCt8Hhd18DuXNiWIse",
    #     role="admin",
    # ),
}

# Populate the database with users
def populate_with_users(users_data: dict[str, UserCreationData]):
    """
    Populates the database with predefined users.
    """
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Required for SQLite
    SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

    try:
        db_session = SessionLocal()

        for user_key, user_data in users_data.items():
            # Check if the user already exists in the database
            result = db_session.query(UserInDb).filter(UserInDb.email == user_data.email).first()
            if not result:
                new_user = UserInDb(email=user_data.email)
                new_user.username = user_data.username
                new_user.role = user_data.role

                # Handle password hashing
                if is_already_hashed(user_data.password):
                    new_user.password_hash = user_data.password  # Directly assign pre-hashed password
                else:
                    new_user.password_hash = get_password_hash(user_data.password)  # Hash plaintext password

                # Handle role-specific logic
                if user_key in ["admin_mike", "active_user"]:
                    new_user.is_active = True
                elif user_key == "inactive_user":
                    new_user.password_hash = get_password_hash(get_old_password(user_data.username))
                    new_user.is_active = False

                try:
                    db_session.add(new_user)
                    db_session.commit()
                    logger.info(f"Added user: {user_data.email}")
                except IntegrityError as e:
                    db_session.rollback()
                    logger.error(f"Error adding user {user_data.email}: {e}")
                except Exception as e:
                    db_session.rollback()
                    logger.error(f"Unexpected error: {e}")

    finally:
        db_session.close()

    logger.info("Database population complete.")

if __name__ == "__main__":
    populate_with_users(object_dict)
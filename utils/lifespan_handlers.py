from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from db.session_provider import get_db_session
from db.token_white_list import clean_tokens
import logging

logger = logging.getLogger(__name__)

# Gestionnaire de lifespan asynchrone
@asynccontextmanager
async def token_cleaner(app: FastAPI):
    try:
        logger.info("Starting token cleanup...")
        db_session = next(get_db_session())
        clean_tokens(db_session)
        logger.info("Token cleanup completed successfully.")
    except Exception as e:
        logger.error(f"Error during token cleanup: {str(e)}")
    finally:
        db_session.close()
        logger.info("Database session closed.")
    yield
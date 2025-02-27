from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

# Application imports
from db.session_provider import get_db_session
from models.models import TokenInDB

def register_token(token: str, expired_time: datetime, db_session: Session) -> None:
    """
    Register a new token in the database.
    """
    try:
        # Ensure expired_time is timezone-aware
        if expired_time.tzinfo is None:
            expired_time = expired_time.replace(tzinfo=timezone.utc)
        db_token = TokenInDB(token=token, expires=expired_time)
        db_session.add(db_token)
        db_session.commit()
        logger.info(f"Registered token: {token} with expiration: {expired_time}")
    except Exception as e:
        logger.error(f"Failed to register token: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to register token: {str(e)}"
        ) from e

def is_valid_token(token: str, db_session: Session) -> bool:
    """
    Check if a token is valid (exists and has not expired).
    """
    try:
        # Fetch the token from the database
        db_token = db_session.query(TokenInDB).filter(TokenInDB.token == token).first()
        if not db_token:
            logger.warning(f"Token not found: {token}")
            return False
        # Ensure both times are timezone-aware
        now = datetime.now(timezone.utc)
        expiration = db_token.expires.replace(tzinfo=timezone.utc)
        # Check if the token has expired
        if now > expiration:
            logger.warning(f"Token expired: {token}")
            return False
        logger.info(f"Token is valid: {token}")
        return True
    except Exception as e:
        logger.error(f"Error validating token: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error validating token: {str(e)}"
        ) from e

def invalidate_token(token: str, db_session: Session) -> None:
    """
    Invalidate a token by removing it from the database.
    """
    try:
        if (
            db_token := db_session.query(TokenInDB)
            .filter(TokenInDB.token == token)
            .first()
        ):
            db_session.delete(db_token)
            db_session.commit()
            logger.info(f"Invalidated token: {token}")
        else:
            logger.warning(f"Token not found: {token}")
    except Exception as e:
        logger.error(f"Error invalidating token: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error invalidating token: {str(e)}"
        ) from e

def clean_tokens(db_session: Session) -> None:
    """
    Clean up expired tokens from the database.
    """
    try:
        # Fetch all tokens
        db_tokens = db_session.query(TokenInDB).all()
        now = datetime.now(timezone.utc)
        if expired_tokens := [
            token
            for token in db_tokens
            if token.expires.replace(tzinfo=timezone.utc) < now
        ]:
            db_session.query(TokenInDB).filter(TokenInDB.token.in_([t.token for t in expired_tokens])).delete(synchronize_session=False)
            db_session.commit()
            logger.info(f"Cleaned up {len(expired_tokens)} expired tokens")
        else:
            logger.info("No expired tokens found")
    except Exception as e:
        logger.error(f"Error cleaning tokens: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error cleaning tokens: {str(e)}"
        ) from e

# Asynchronous context manager for lifespan cleanup
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
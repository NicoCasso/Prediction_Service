from fastapi import FastAPI
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session
from db.session_provider import get_db_session
from db.token_white_list import clean_tokens

# Gestionnaire de lifespan asynchrone
@asynccontextmanager
async def token_cleaner(app: FastAPI):
    db_session = next(get_db_session())
    clean_tokens(db_session)  
    yield  
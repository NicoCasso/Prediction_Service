from fastapi import Depends
from db.session_provider import get_db_session
from sqlalchemy.orm import Session
from datetime import datetime, timezone

#application imports
from models.models import TokenInDB

def register_token(token : str, expired_time: datetime, db_session : Session ):
    db_token  = TokenInDB(expires = expired_time, token = token)
    db_session.add(db_token)
    db_session.commit()

def is_valid_token(token : str, db_session : Session) -> bool :
    db_token = db_session.query(TokenInDB).where(TokenInDB.token==token).first()
    if not db_token :
        return False
    
    if db_token.expires > datetime.now(timezone.utc) :
        return False
    
    return True
    
def invalidate_token(token : str, db_session : Session)  :
    db_token = db_session.query(TokenInDB).where(TokenInDB.token==token).first()
    if db_token :
        db_session.delete(db_token)
        db_session.commit()

def clean_tokens(db_session : Session) : 
    now = datetime.now(timezone.utc) 
    db_tokens = db_session.query(TokenInDB).all()
    for db_token in db_tokens :
        if db_token.expires > now :
            db_session.delete(db_token)

    db_session.commit()


    

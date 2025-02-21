from fastapi import Depends
from db.session_provider import get_db_session
#from sqlmodel import Session, select
from sqlalchemy.orm import Session

from datetime import datetime, timezone

#application imports
from models.models import TokenInDB

def register_token(token : str, expired_time: datetime, db_session : Session ):
    db_token  = TokenInDB(expires = expired_time, token = token)
    db_session.add(db_token)
    db_session.commit()

def is_valid_token(token : str, db_session : Session) -> bool :

    # statement = select(TokenInDB).where(TokenInDB.token==token)
    # db_token = db_session.exec(statement).one_or_none()

    db_token = db_session.query(TokenInDB).filter(TokenInDB.token == token).first()

    if not db_token :
        return False
    
    now = datetime.now(timezone.utc)
    expiration = db_token.expires.replace(tzinfo=timezone.utc)

    if now > expiration :
        return False
    
    return True
    
def invalidate_token(token : str, db_session : Session)  :

    # statement = select(TokenInDB).where(TokenInDB.token==token)
    # db_token = db_session.exec(statement).one_or_none()

    db_token = db_session.query(TokenInDB).filter(TokenInDB.token==token).first()
 
    if db_token :
        db_session.delete(db_token)
        db_session.commit()

def clean_tokens(db_session: Session) : 
    now = datetime.now(timezone.utc) 

    # statement = select(TokenInDB)
    # db_tokens = db_session.exec(statement).all()

    db_tokens = db_session.query(TokenInDB).all()

    now = datetime.now(timezone.utc)
    
    for db_token in db_tokens :
        expiration = db_token.expires.replace(tzinfo=timezone.utc)
        if now > expiration :
            db_session.delete(db_token)

    db_session.commit()
    #db_session.refresh()


    

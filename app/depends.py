from fastapi import Depends
from app.db.connection import Session

def get_db_session():
    try:
        db = Session()
        yield db
    finally:
        db.close()
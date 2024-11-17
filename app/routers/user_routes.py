from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.auth_user import UserAuth
from app.depends import get_db_session
from app.schemas import User

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: User, db: Session = Depends(get_db_session)) -> User:
    user_auth = UserAuth(db)
    return user_auth.create_user(user)
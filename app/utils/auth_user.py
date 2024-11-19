from datetime import datetime, timedelta, timezone
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
from app.db.models import UserModel
from app.schemas import LoginResponse, User
from decouple import config
from jose import jwt
from passlib.context import CryptContext


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
crypt_context = CryptContext(schemes=["sha256_crypt"])

class UserAuth:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        db_user = UserModel(
            email=user.email,
            full_name=user.full_name,
            password=self.get_password_hash(user.password),
            community_id=user.community_id,
            is_manager=user.is_manager | False
        )
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário já cadastrado")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def login_user(self, email: str, password: str, expires_in: int = 30) -> LoginResponse:
        user = self.get_user_by_email(email)
        if not self.verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos")
        
        access_token = self.create_access_token(data={"sub": user.email}, expires_in=expires_in)
        return {"access_token": access_token[0], "token_type": "bearer", "expires_in": access_token[1]}

    def create_access_token(self, data: dict, expires_in: int) -> str:
        to_encode = data.copy()
        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
        to_encode.update({"exp": exp})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return [encoded_jwt, exp.isoformat()]

    def get_user_by_email(self, email: str) -> User:
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos")
        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return crypt_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return crypt_context.hash(password)
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
from app.db.models import UserModel
from app.schemas import User
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["sha256_crypt"])

class UserAuth:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        db_user = UserModel(
            email=user.email,
            full_name=user.full_name,
            password=self.get_password_hash(user.password),
            community=user.community,
            is_manager=user.is_manager
        )
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário já cadastrado")
        return db_user
    
    def login_user(self, email: str, password: str) -> User:
        user = self.get_user_by_email(email)
        if not self.verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return crypt_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return crypt_context.hash(password)
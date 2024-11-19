from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth_user import UserAuth
from app.depends import get_db_session
from app.schemas import DefaultResponse, HTTPErrorRequest, LoginResponse, User

user_router = APIRouter(prefix="/user", tags=["User"])

class OAuth2PasswordRequestFormEmail(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(default=None, description="Grant type"),
        email: str = Form(..., description="User email"),  # Torna obrigatório com "..."
        password: str = Form(..., description="User password"),  # Torna obrigatório
        scope: str = Form(default=""),
        client_id: str = Form(default=None),
        client_secret: str = Form(default=None),
    ):
        super().__init__(
            grant_type=grant_type,
            username=email,  # Mapear "username" para "email"
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )

@user_router.post("/register", response_model=DefaultResponse, status_code=status.HTTP_201_CREATED, responses={400: {"description": "Usuário já cadastrado", "model": DefaultResponse}})
def register_user(user: User, db: Session = Depends(get_db_session)) -> User:
    user_auth = UserAuth(db)
    user_auth.create_user(user)
    return JSONResponse(content={'msg':'Sucesso na criação do usuário'} ,status_code=status.HTTP_201_CREATED)

@user_router.post(
    "/login", 
    response_model=LoginResponse, 
    status_code=status.HTTP_200_OK, 
    responses={401: {"description": "Email ou senha inválidos", "model": HTTPErrorRequest}}
)
def login_user(
    email: str = Form(..., description="Email do usuário"),
    password: str = Form(..., description="Senha do usuário"),
    db: Session = Depends(get_db_session),
) -> LoginResponse:
    user_auth = UserAuth(db)
    auth_data = user_auth.login_user(email, password)
    return auth_data
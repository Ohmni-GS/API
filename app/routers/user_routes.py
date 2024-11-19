from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth_user import UserAuth
from app.depends import get_db_session
from app.schemas import DefaultResponse, HTTPErrorRequest, LoginResponse, User, UserUpdate, UserWithoutPassword

user_router = APIRouter(prefix="/users", tags=["Users"])

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

@user_router.get("/", response_model=list[UserWithoutPassword], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db_session)) -> list[UserWithoutPassword]:
    user_auth = UserAuth(db)
    users = user_auth.get_users()
    for user in users:
        user.password = None
    return users

@user_router.get("/{email}", response_model=UserWithoutPassword, status_code=status.HTTP_200_OK , responses={404: {"description": "Usuário não encontrado", "model": HTTPErrorRequest}})
def get_user(email: str, db: Session = Depends(get_db_session)) -> UserWithoutPassword:
    user_auth = UserAuth(db)
    user = user_auth.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    user.password = None
    return user

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


@user_router.post("/token", response_model=DefaultResponse, status_code=status.HTTP_200_OK, responses={401: {"description": "Token inválido", "model": HTTPErrorRequest}})
def verify_token(token: str = Form(..., description="Token de acesso"), db: Session = Depends(get_db_session)) -> DefaultResponse:
    user_auth = UserAuth(db)
    user_auth.verify_token(token)
    return JSONResponse(content={'msg':'Token válido'} ,status_code=status.HTTP_200_OK)

@user_router.delete("/{email}", response_model=DefaultResponse, status_code=status.HTTP_200_OK, responses={404: {"description": "Usuário não encontrado", "model": HTTPErrorRequest}})
def delete_user(email: str, db: Session = Depends(get_db_session)) -> DefaultResponse:
    user_auth = UserAuth(db)
    user_auth.delete_user(email)
    return JSONResponse(content={'msg':'Usuário deletado com sucesso'} ,status_code=status.HTTP_200_OK)

@user_router.put("/{email}", response_model=DefaultResponse, status_code=status.HTTP_200_OK, responses={404: {"description": "Usuário não encontrado", "model": HTTPErrorRequest}})
def update_user(email: str, user_update: UserUpdate, db: Session = Depends(get_db_session)) -> DefaultResponse:
    user_auth = UserAuth(db)
    user_auth.update_user(email, user_update)
    return JSONResponse(content={'msg': 'Usuário atualizado com sucesso'}, status_code=status.HTTP_200_OK)

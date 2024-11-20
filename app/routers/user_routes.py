from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.users import UsersService
from app.depends import get_db_session
from app.schemas import DefaultResponse, HTTPErrorRequest, LoginResponse, User, UserUpdate, UserWithoutPassword

user_router = APIRouter(prefix="/users", tags=["Users"])

def get_users_service(db: Session = Depends(get_db_session)) -> UsersService:
    return UsersService(db=db)

@user_router.get("/", response_model=list[UserWithoutPassword], status_code=status.HTTP_200_OK)
def get_users(users_service: UsersService = Depends(get_users_service)) -> list[UserWithoutPassword]:
    users = users_service.get_users()
    for user in users:
        user.password = None
    return users

@user_router.get("/{id}", response_model=UserWithoutPassword, status_code=status.HTTP_200_OK , responses={404: {"description": "Usuário não encontrado", "model": HTTPErrorRequest}})
def get_user(id: str, users_service: UsersService = Depends(get_users_service)) -> UserWithoutPassword:
    user = users_service.get_user_by_id(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    user.password = None
    return user

@user_router.post("/register", response_model=DefaultResponse, status_code=status.HTTP_201_CREATED, responses={400: {"description": "Usuário já cadastrado", "model": DefaultResponse}})
def register_user(user: User, users_service: UsersService = Depends(get_users_service)) -> User:
    users_service.create_user(user)
    return DefaultResponse(msg='Usuário cadastrado com sucesso')

@user_router.post(
    "/login", 
    response_model=LoginResponse, 
    status_code=status.HTTP_200_OK, 
    responses={401: {"description": "Email ou senha inválidos", "model": HTTPErrorRequest}}
)
def login_user(
    email: str = Form(..., description="Email do usuário"),
    password: str = Form(..., description="Senha do usuário"),
    users_service: UsersService = Depends(get_users_service),
) -> LoginResponse:
    auth_data = users_service.login_user(email, password)
    return auth_data


@user_router.post("/token", response_model=DefaultResponse, status_code=status.HTTP_200_OK, responses={401: {"description": "Token inválido", "model": HTTPErrorRequest}})
def verify_token(token: str = Form(..., description="Token de acesso"), users_service: UsersService = Depends(get_users_service)) -> DefaultResponse:
    users_service.verify_token(token)
    return DefaultResponse(msg='Token válido')

@user_router.delete("/{id}", response_model=DefaultResponse, status_code=status.HTTP_200_OK, responses={404: {"description": "Usuário não encontrado", "model": HTTPErrorRequest}})
def delete_user(id: str, users_service: UsersService = Depends(get_users_service)) -> DefaultResponse:
    users_service.delete_user(id)
    return DefaultResponse(msg='Usuário deletado com sucesso')

@user_router.put("/{id}", response_model=DefaultResponse, status_code=status.HTTP_200_OK, responses={404: {"description": "Usuário não encontrado", "model": HTTPErrorRequest}})
def update_user(id: str, user_update: UserUpdate, users_service: UsersService = Depends(get_users_service)) -> DefaultResponse:
    users_service.update_user(id, user_update)
    return DefaultResponse(msg='Usuário atualizado com sucesso')

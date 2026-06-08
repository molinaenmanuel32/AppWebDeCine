# cinemax/api/routers/auth.py
"""Router de autenticación."""

from fastapi import APIRouter, Depends
from ..schemas.auth import UserRegister, UserLogin, UserResponse, TokenResponse
from ..services.auth_service import AuthService, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


def _service() -> AuthService:
    return AuthService()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: UserRegister, service: AuthService = Depends(_service)):
    return service.register(payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, service: AuthService = Depends(_service)):
    return service.login(payload)


@router.get("/me", response_model=UserResponse)
def me(current_user: UserResponse = Depends(get_current_user)):
    return current_user

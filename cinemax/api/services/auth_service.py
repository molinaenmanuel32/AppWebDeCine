# cinemax/api/services/auth_service.py
"""Servicio de autenticación: JWT + bcrypt."""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Dict, Optional

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ..repositories.user_repository import UserRepository
from ..schemas.auth import UserRegister, UserLogin, UserResponse, TokenResponse

SECRET_KEY = os.getenv("JWT_SECRET", "change_me_in_production_please")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def _hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def _verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def _create_token(data: Dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


class AuthService:

    def __init__(self) -> None:
        self._repo = UserRepository()

    def register(self, payload: UserRegister) -> UserResponse:
        if self._repo.find_by_email(payload.email):
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        hashed = _hash_password(payload.password)
        new_id = self._repo.create(payload.name, payload.email, hashed)
        user = self._repo.find_by_id(new_id)
        return UserResponse(**user)

    def login(self, payload: UserLogin) -> TokenResponse:
        user = self._repo.find_by_email(payload.email)
        if not user or not _verify_password(payload.password, user["password"]):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        token = _create_token({"sub": str(user["id"]), "role": user["role"]})
        return TokenResponse(
            access_token=token,
            user=UserResponse(**{k: v for k, v in user.items() if k != "password"}),
        )


# ── Dependency injection ───────────────────────────────────────────────────────
def _decode_token(token: str) -> Dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    payload = _decode_token(token)
    repo = UserRepository()
    user = repo.find_by_id(int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return UserResponse(**user)


def require_admin(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """Dependency que lanza 403 si el usuario no es admin."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: se requiere rol admin",
        )
    return current_user

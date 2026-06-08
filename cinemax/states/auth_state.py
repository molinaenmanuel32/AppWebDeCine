# cinemax/states/auth_state.py
"""
Estado de autenticación Reflex.
Almacena: token JWT, datos del usuario y su role durante toda la sesión.
Principio SRP: solo gestiona auth — el resto de estados lo extienden.
"""

from __future__ import annotations

import os

import httpx
import reflex as rx

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


class AuthState(rx.State):
    # ── Campos de sesión ──────────────────────────────────────────────────────
    token: str = ""
    user_id: int = 0
    user_name: str = ""
    user_email: str = ""
    user_role: str = ""  # "user" | "admin" | ""

    # UI
    is_loading: bool = False
    error_message: str = ""

    # ── Computed ──────────────────────────────────────────────────────────────
    @rx.var
    def is_authenticated(self) -> bool:
        return bool(self.token)

    @rx.var
    def is_admin(self) -> bool:
        return self.user_role == "admin"

    # ── Private helpers ───────────────────────────────────────────────────────
    def _auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    def _set_error(self, msg: str) -> None:
        self.error_message = msg
        self.is_loading = False

    def _clear_error(self) -> None:
        self.error_message = ""

    # ── Actions ───────────────────────────────────────────────────────────────
    async def login(self, form_data: dict):
        self._clear_error()
        self.is_loading = True
        yield

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{API_BASE}/auth/login",
                    json={
                        "email": form_data["email"],
                        "password": form_data["password"],
                    },
                    timeout=10,
                )

            if resp.status_code == 200:
                data = resp.json()

                self.token = data["access_token"]

                user = data["user"]
                self.user_id = user["id"]
                self.user_name = user["name"]
                self.user_email = user["email"]
                self.user_role = user["role"]

                self.is_loading = False
                yield

                # Redirigir según rol
                if self.user_role == "admin":
                    yield rx.redirect("/admin")
                else:
                    yield rx.redirect("/")

            else:
                self._set_error(
                    resp.json().get("detail", "Error al iniciar sesión")
                )
                yield

        except Exception as e:
            self._set_error(f"Error de conexión: {str(e)}")
            yield

    async def register(self, form_data: dict):
        self._clear_error()
        self.is_loading = True
        yield

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{API_BASE}/auth/register",
                    json={
                        "name": form_data["name"],
                        "email": form_data["email"],
                        "password": form_data["password"],
                    },
                    timeout=10,
                )

            if resp.status_code == 201:
                self.is_loading = False
                yield
                yield rx.redirect("/login")

            else:
                self._set_error(
                    resp.json().get("detail", "Error al registrarse")
                )
                yield

        except Exception as e:
            self._set_error(f"Error de conexión: {str(e)}")
            yield

    def logout(self):
        self.token = ""
        self.user_id = 0
        self.user_name = ""
        self.user_email = ""
        self.user_role = ""
        self.error_message = ""
        return rx.redirect("/")
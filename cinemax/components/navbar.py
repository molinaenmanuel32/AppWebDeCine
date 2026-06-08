# cinemax/components/navbar.py

"""
Navbar principal.
Muestra el enlace "Administración" SOLO cuando el usuario es admin.
Usa AuthState como fuente única de autenticación.
"""

import reflex as rx
from ..states.auth_state import AuthState


def _nav_link(text: str, href: str) -> rx.Component:
    return rx.link(
        text,
        href=href,
        color="white",
        font_weight="500",
        _hover={"color": "#E50914", "text_decoration": "none"},
        transition="color 0.2s",
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Logo
            rx.link(
                rx.hstack(
                    rx.icon("film", color="#E50914", size=28),
                    rx.text(
                        "CINEMAX",
                        font_size="1.4rem",
                        font_weight="800",
                        color="white",
                        letter_spacing="0.1em",
                    ),
                    spacing="2",
                ),
                href="/",
                _hover={"text_decoration": "none"},
            ),

            rx.spacer(),

            # Links públicos
            rx.hstack(
                _nav_link("Inicio", "/"),
                _nav_link("Catálogo", "/catalogo"),

                # Visible solo para admins
                rx.cond(
                    AuthState.is_admin,
                    _nav_link("⚙ Administración", "/admin"),
                    rx.fragment(),
                ),

                spacing="6",
            ),

            rx.spacer(),

            # Zona autenticación
            rx.cond(
                AuthState.is_authenticated,

                # Usuario logueado
                rx.hstack(
                    rx.text(
                        AuthState.user_name,
                        color="#aaa",
                        font_size="0.9rem",
                    ),

                    rx.cond(
                        AuthState.is_admin,
                        rx.badge(
                            "ADMIN",
                            color_scheme="red",
                            variant="solid",
                        ),
                        rx.fragment(),
                    ),

                    rx.link(
                        rx.button(
                            "Mis Reservas",
                            variant="ghost",
                            color="white",
                            size="2",
                            _hover={"bg": "#222"},
                        ),
                        href="/mis-reservas",
                    ),

                    rx.button(
                        "Salir",
                        on_click=AuthState.logout,
                        variant="outline",
                        color_scheme="red",
                        size="2",
                    ),

                    spacing="3",
                    align="center",
                ),

                # Usuario no autenticado
                rx.hstack(
                    rx.link(
                        rx.button(
                            "Iniciar sesión",
                            variant="ghost",
                            color="white",
                            _hover={"bg": "#222"},
                        ),
                        href="/login",
                    ),

                    rx.link(
                        rx.button(
                            "Registrarse",
                            bg="#E50914",
                            color="white",
                            _hover={"bg": "#b0060f"},
                        ),
                        href="/registro",
                    ),

                    spacing="3",
                ),
            ),
        ),

        bg="#0a0a0a",
        border_bottom="1px solid #1a1a1a",
        px="8",
        py="4",
        position="sticky",
        top="0",
        z_index="100",
        width="100%",
    )
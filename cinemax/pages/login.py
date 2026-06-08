"""
pages/login.py
Página de login con glassmorphism.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.components.navbar import navbar
from cinemax.components.toast import toast
from cinemax.states.app_state import AppState


@rx.page(route="/login", title="Login - CineMax")
def login_page() -> rx.Component:
    return rx.box(
        navbar(),

        rx.box(
            rx.box(
                position="absolute", top="-200px", right="-200px",
                width="600px", height="600px",
                background="radial-gradient(circle, rgba(229,9,20,0.08) 0%, transparent 70%)",
                pointer_events="none",
            ),

            rx.box(
                rx.vstack(
                    rx.vstack(
                        rx.hstack(
                            rx.text("K", color=RED_CINE, font_size="2.5rem", font_family=FONT_HEADING),
                            rx.text("ANKYCINE", color=WHITE, font_size="2.5rem", font_family=FONT_HEADING),
                            spacing="0",
                        ),
                        rx.text("Inicia sesión en tu cuenta", color=GRAY_MUTED, font_size="15px"),
                        align_items="center",
                        spacing="1",
                        margin_bottom="1rem",
                    ),

                    rx.cond(
                        AppState.auth_error != "",
                        rx.box(
                            rx.hstack(
                                rx.icon("circle-x", size=16, color=RED_CINE),
                                rx.text(AppState.auth_error, color=RED_CINE, font_size="14px"),
                                spacing="2", align="center",
                            ),
                            background="rgba(229,9,20,0.1)",
                            border="1px solid rgba(229,9,20,0.3)",
                            border_radius="8px",
                            padding="10px 14px",
                            width="100%",
                        ),
                    ),

                    rx.vstack(
                        rx.text("Correo electrónico", color=WHITE_SOFT, font_size="13px", font_weight="600"),
                        rx.box(
                            rx.hstack(
                                rx.icon("mail", size=16, color=GRAY_MUTED),
                                rx.input(
                                    placeholder="tu@email.com",
                                    on_change=AppState.set_login_email,
                                    value=AppState.login_email,
                                    type="email",
                                    background="transparent",
                                    border="none",
                                    color=WHITE,
                                    flex="1",
                                    font_size="15px",
                                    _focus={"outline": "none"},
                                    _placeholder={"color": GRAY_MUTED},
                                ),
                                align="center",
                                spacing="3",
                            ),
                            background=GRAY_DARK,
                            border="1px solid rgba(255,255,255,0.1)",
                            border_radius="10px",
                            padding="12px 16px",
                            _focus_within={
                                "border_color": RED_CINE,
                                "box_shadow": "0 0 0 3px rgba(229,9,20,0.15)",
                            },
                        ),
                        align_items="start",
                        spacing="2",
                        width="100%",
                    ),

                    rx.vstack(
                        rx.hstack(
                            rx.text("Contraseña", color=WHITE_SOFT, font_size="13px", font_weight="600"),
                            rx.link("¿Olvidaste tu contraseña?", href="#", color=GRAY_MUTED, font_size="12px", text_decoration="none", _hover={"color": WHITE}),
                            justify="between",
                            width="100%",
                        ),
                        rx.box(
                            rx.hstack(
                                rx.icon("lock", size=16, color=GRAY_MUTED),
                                rx.input(
                                    placeholder="••••••••",
                                    on_change=AppState.set_login_password,
                                    value=AppState.login_password,
                                    type="password",
                                    background="transparent",
                                    border="none",
                                    color=WHITE,
                                    flex="1",
                                    font_size="15px",
                                    _focus={"outline": "none"},
                                    _placeholder={"color": GRAY_MUTED},
                                ),
                                align="center",
                                spacing="3",
                            ),
                            background=GRAY_DARK,
                            border="1px solid rgba(255,255,255,0.1)",
                            border_radius="10px",
                            padding="12px 16px",
                            _focus_within={
                                "border_color": RED_CINE,
                                "box_shadow": "0 0 0 3px rgba(229,9,20,0.15)",
                            },
                        ),
                        align_items="start",
                        spacing="2",
                        width="100%",
                    ),

                    rx.button(
                        "Iniciar Sesión",
                        on_click=AppState.handle_login,
                        background=RED_CINE,
                        color=WHITE,
                        border="none",
                        border_radius="10px",
                        padding="14px",
                        font_size="15px",
                        font_weight="700",
                        cursor="pointer",
                        width="100%",
                        transition="all 0.2s ease",
                        _hover={"background": RED_HOVER, "transform": "translateY(-1px)", "box_shadow": "0 8px 24px rgba(229,9,20,0.4)"},
                    ),

                    rx.hstack(
                        rx.text("¿No tienes cuenta?", color=GRAY_MUTED, font_size="14px"),
                        rx.link("Regístrate gratis", href="/registro", color=RED_CINE, font_size="14px", font_weight="600", text_decoration="none", _hover={"color": RED_HOVER}),
                        spacing="2",
                        justify="center",
                    ),

                    align_items="start",
                    spacing="5",
                    width="100%",
                ),

                background="rgba(26,26,26,0.95)",
                backdrop_filter="blur(20px)",
                border="1px solid rgba(255,255,255,0.08)",
                border_radius="20px",
                padding="2.5rem",
                width="100%",
                max_width="440px",
                box_shadow="0 24px 64px rgba(0,0,0,0.8)",
            ),

            display="flex",
            align_items="center",
            justify_content="center",
            min_height="100vh",
            padding=["1.5rem", "2rem"],
            position="relative",
            overflow="hidden",
        ),

        toast(),
        background=BLACK_CINEMA,
        font_family=FONT_BODY,
    )

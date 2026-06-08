"""
pages/registro.py
Página de registro premium.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.components.navbar import navbar
from cinemax.components.toast import toast
from cinemax.states.app_state import AppState


def form_field(label: str, placeholder: str, field_type: str, value, on_change, icon: str = "user") -> rx.Component:
    return rx.vstack(
        rx.text(label, color=WHITE_SOFT, font_size="13px", font_weight="600"),
        rx.box(
            rx.hstack(
                rx.icon(icon, size=16, color=GRAY_MUTED),
                rx.input(
                    placeholder=placeholder,
                    on_change=on_change,
                    value=value,
                    type=field_type,
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
    )


@rx.page(route="/registro", title="Registro - CineMax")
def registro_page() -> rx.Component:
    return rx.box(
        navbar(),

        rx.box(
            rx.box(
                position="absolute", top="-100px", left="-100px",
                width="500px", height="500px",
                background="radial-gradient(circle, rgba(229,9,20,0.07) 0%, transparent 70%)",
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
                        rx.text("Crea tu cuenta premium", color=GRAY_MUTED, font_size="15px"),
                        align_items="center",
                        spacing="1",
                        margin_bottom="0.5rem",
                    ),

                    rx.hstack(
                        rx.icon("star", size=14, color=GOLD_VIP),
                        rx.text("Primer mes VIP gratis al registrarte", color=GOLD_VIP, font_size="13px", font_weight="600"),
                        spacing="2",
                        align="center",
                        background="rgba(245,197,24,0.08)",
                        border="1px solid rgba(245,197,24,0.2)",
                        border_radius="8px",
                        padding="8px 16px",
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

                    form_field("Nombre completo", "John Doe", "text", AppState.register_name, AppState.set_register_name, "user"),
                    form_field("Correo electrónico", "tu@email.com", "email", AppState.register_email, AppState.set_register_email, "mail"),
                    form_field("Contraseña", "Mínimo 8 caracteres", "password", AppState.register_password, AppState.set_register_password, "lock"),
                    form_field("Confirmar contraseña", "Repite tu contraseña", "password", AppState.register_confirm, AppState.set_register_confirm, "lock"),

                    rx.button(
                        "Crear Cuenta Premium",
                        on_click=AppState.handle_register,
                        background=f"linear-gradient(135deg, {RED_CINE}, {RED_DARK})",
                        color=WHITE,
                        border="none",
                        border_radius="10px",
                        padding="14px",
                        font_size="15px",
                        font_weight="700",
                        cursor="pointer",
                        width="100%",
                        transition="all 0.2s ease",
                        _hover={"transform": "translateY(-1px)", "box_shadow": "0 8px 24px rgba(229,9,20,0.4)"},
                    ),

                    rx.hstack(
                        rx.text("¿Ya tienes cuenta?", color=GRAY_MUTED, font_size="14px"),
                        rx.link("Iniciar sesión", href="/login", color=RED_CINE, font_size="14px", font_weight="600", text_decoration="none", _hover={"color": RED_HOVER}),
                        spacing="2",
                        justify="center",
                    ),

                    align_items="start",
                    spacing="4",
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
            padding_top=["5rem", "5rem"],
            position="relative",
            overflow="hidden",
        ),

        toast(),
        background=BLACK_CINEMA,
        font_family=FONT_BODY,
    )

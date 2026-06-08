"""
components/toast.py
Notificaciones toast animadas.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.states.app_state import AppState


def toast() -> rx.Component:
    return rx.cond(
        AppState.toast_visible,
        rx.box(
            rx.hstack(
                rx.cond(
                    AppState.toast_type == "success",
                    rx.icon("circle-check", size=18, color="#22c55e"),
                    rx.cond(
                        AppState.toast_type == "error",
                        rx.icon("circle-x", size=18, color=RED_CINE),
                        rx.icon("info", size=18, color="#3b82f6"),
                    ),
                ),
                rx.text(AppState.toast_message, color=WHITE, font_size="14px", font_weight="500"),
                rx.button(
                    rx.icon("x", size=14),
                    on_click=AppState.hide_toast,
                    background="transparent",
                    border="none",
                    color=WHITE_MUTED,
                    cursor="pointer",
                    padding="0",
                    _hover={"color": WHITE},
                ),
                align="center",
                justify="between",
                spacing="3",
                width="100%",
            ),
            position="fixed",
            bottom="2rem",
            right="2rem",
            background=GRAY_DARK,
            border="1px solid rgba(255,255,255,0.1)",
            border_radius="12px",
            padding="14px 18px",
            z_index="9999",
            min_width="280px",
            max_width="400px",
            box_shadow="0 8px 32px rgba(0,0,0,0.6)",
            animation="slideInRight 0.3s ease",
        ),
    )

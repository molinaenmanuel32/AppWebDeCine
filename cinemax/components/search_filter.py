"""
components/search_filter.py
Barra de búsqueda y chips de filtro por categorías.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.states.app_state import AppState


CATEGORIES = ["Todos", "Acción", "Terror", "Comedia", "Ciencia Ficción", "Drama", "Infantil"]


def search_bar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("search", size=18, color=GRAY_MUTED),
            rx.input(
                placeholder="Buscar películas...",
                on_change=AppState.set_search,
                value=AppState.search_query,
                background="transparent",
                border="none",
                color=WHITE,
                flex="1",
                font_size="15px",
                _focus={"outline": "none"},
                _placeholder={"color": GRAY_MUTED},
            ),
            rx.cond(
                AppState.search_query != "",
                rx.button(
                    rx.icon("x", size=14),
                    on_click=AppState.set_search(""),
                    background="transparent",
                    border="none",
                    color=GRAY_MUTED,
                    cursor="pointer",
                    padding="0",
                    _hover={"color": WHITE},
                ),
            ),
            align="center",
            padding="12px 16px",
            spacing="3",
            background=GRAY_DARK,
            border="1px solid rgba(255,255,255,0.08)",
            border_radius="12px",
            _focus_within={
                "border_color": RED_CINE,
                "box_shadow": "0 0 0 3px rgba(229,9,20,0.15)",
            },
        ),
        width="100%",
        max_width="480px",
    )


def category_chip(label: str) -> rx.Component:
    is_active = AppState.active_category == label

    return rx.button(
        label,
        on_click=AppState.set_category(label),
        background=rx.cond(is_active, RED_CINE, "rgba(255,255,255,0.06)"),
        color=rx.cond(is_active, WHITE, WHITE_MUTED),
        border=rx.cond(
            is_active,
            f"1px solid {RED_CINE}",
            "1px solid rgba(255,255,255,0.1)",
        ),
        border_radius="30px",
        padding="8px 18px",
        font_size="13px",
        font_weight=rx.cond(is_active, "700", "500"),
        cursor="pointer",
        transition="all 0.2s ease",
        white_space="nowrap",
        _hover={
            "background": rx.cond(is_active, RED_HOVER, "rgba(255,255,255,0.12)"),
            "transform": "translateY(-1px)",
        },
    )


def category_filter() -> rx.Component:
    return rx.box(
        rx.hstack(
            *[category_chip(cat) for cat in CATEGORIES],
            spacing="2",
            overflow_x="auto",
            padding_bottom="4px",
            flex_wrap="wrap",
        ),
    )


def sort_select() -> rx.Component:
    return rx.select(
        ["nombre", "precio", "duracion"],
        placeholder="Ordenar por...",
        on_change=AppState.set_sort,
        background=GRAY_DARK,
        color=WHITE,
        border="1px solid rgba(255,255,255,0.08)",
        border_radius="8px",
        font_size="13px",
    )

"""
pages/catalogo.py
Página catálogo completa con búsqueda, filtros y grid responsive.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.components.navbar import navbar
from cinemax.components.footer import footer
from cinemax.components.toast import toast
from cinemax.components.movie_card import movie_card
from cinemax.components.search_filter import search_bar, category_filter, sort_select
from cinemax.states.app_state import AppState


@rx.page(route="/catalogo", title="Catálogo - CineMax", on_load=AppState.on_load)
def catalogo_page() -> rx.Component:
    return rx.box(
        navbar(),

        rx.box(
            # Page Header
            rx.box(
                rx.vstack(
                    rx.text(
                        "CARTELERA",
                        font_family=FONT_HEADING,
                        font_size=["3rem", "4rem", "5rem"],
                        color=WHITE,
                        letter_spacing="1",
                    ),
                    rx.box(width="64px", height="5px", background=RED_CINE, border_radius="2px"),
                    rx.text(
                        "Descubre las mejores películas del momento",
                        color=GRAY_MUTED,
                        font_size="16px",
                    ),
                    align_items="start",
                    spacing="2",
                ),
                padding=["6rem 1.5rem 2rem", "7rem 2rem 2rem", "8rem 4rem 2rem"],
                background="linear-gradient(180deg, rgba(229,9,20,0.05) 0%, transparent 100%)",
                border_bottom="1px solid rgba(255,255,255,0.05)",
            ),

            # Search & Filters
            rx.box(
                rx.flex(
                    search_bar(),
                    sort_select(),
                    gap="1rem",
                    flex_wrap="wrap",
                    align_items="center",
                    margin_bottom="1.5rem",
                ),
                category_filter(),
                padding=["1.5rem", "1.5rem 2rem", "2rem 4rem"],
                border_bottom="1px solid rgba(255,255,255,0.05)",
                background=GRAY_DARK,
            ),

            # Filter indicator
            rx.box(
                rx.hstack(
                    rx.cond(
                        AppState.active_category != "Todos",
                        rx.hstack(
                            rx.text("Filtrando por:", color=GRAY_MUTED, font_size="13px"),
                            rx.box(
                                AppState.active_category,
                                background="rgba(229,9,20,0.15)",
                                color=RED_CINE,
                                font_size="12px",
                                padding="3px 12px",
                                border_radius="20px",
                            ),
                            spacing="2",
                            align="center",
                        ),
                    ),
                    spacing="4",
                    align="center",
                ),
                padding=["1rem 1.5rem", "1rem 2rem", "1rem 4rem"],
            ),

            # Movie Grid
            rx.box(
                rx.cond(
                    AppState.filtered_movies.length() == 0,
                    rx.vstack(
                        rx.icon("film", size=48, color=GRAY_MUTED),
                        rx.text("No se encontraron películas", color=WHITE_MUTED, font_size="18px", font_weight="600"),
                        rx.text("Intenta con otros filtros o términos de búsqueda.", color=GRAY_MUTED, font_size="14px"),
                        align_items="center",
                        spacing="3",
                        padding="5rem 0",
                        width="100%",
                    ),
                    rx.grid(
                        rx.foreach(AppState.filtered_movies, movie_card),
                        template_columns=[
                            "repeat(2, 1fr)",
                            "repeat(3, 1fr)",
                            "repeat(4, 1fr)",
                            "repeat(5, 1fr)",
                        ],
                        gap="1.5rem",
                        width="100%",
                    ),
                ),
                padding=["1.5rem", "2rem", "2rem 4rem"],
                min_height="50vh",
            ),

            background=BLACK_CINEMA,
            min_height="100vh",
        ),

        footer(),
        toast(),
        font_family=FONT_BODY,
        background=BLACK_CINEMA,
    )

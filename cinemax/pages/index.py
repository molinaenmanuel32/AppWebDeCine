"""
pages/index.py
Página principal — Home de Cinemax.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.components.navbar import navbar
from cinemax.components.footer import footer
from cinemax.components.toast import toast
from cinemax.components.hero import hero_section
from cinemax.components.carousel import movie_carousel
from cinemax.components.vip_section import vip_section
from cinemax.states.app_state import AppState


@rx.page(route="/", title="Inicio - CineMax", on_load=AppState.on_load)
def index_page() -> rx.Component:
    return rx.box(
        navbar(),

        rx.box(
            hero_section(),

            # Carrusel principal
            rx.box(
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.text("EN CARTELERA", font_family=FONT_HEADING, font_size="2rem", color=WHITE, letter_spacing="1"),
                            rx.box(width="48px", height="4px", background=RED_CINE, border_radius="2px"),
                            rx.text("Las últimas incorporaciones", color=GRAY_MUTED, font_size="14px"),
                            align_items="start",
                            spacing="2",
                        ),
                        rx.link(
                            rx.hstack(
                                rx.text("Ver todo", color=GRAY_MUTED, font_size="14px"),
                                rx.icon("arrow-right", size=14, color=GRAY_MUTED),
                                spacing="2",
                                align="center",
                            ),
                            href="/catalogo",
                            text_decoration="none",
                            color=GRAY_MUTED,
                        ),
                        justify="between",
                        align="end",
                        width="100%",
                        margin_bottom="1.5rem",
                    ),
                    rx.box(
                        rx.hstack(
                            rx.foreach(AppState.movies, _movie_card_carousel),
                            spacing="4",
                            align="stretch",
                        ),
                        overflow_x="auto",
                        padding_bottom="16px",
                    ),
                    padding="0 2rem",
                    max_width="1400px",
                    margin="0 auto",
                    width="100%",
                ),
                padding="3rem 0",
            ),

            # VIP Section
            vip_section(),

            # Promo Banner
            rx.box(
                rx.box(
                    rx.vstack(
                        rx.text("🎬 MARTES DE CINE", font_size="12px", color=RED_CINE, font_weight="800", letter_spacing="1"),
                        rx.text(
                            "2x1 en todas las funciones",
                            font_family=FONT_HEADING,
                            font_size=["2rem", "3rem"],
                            color=WHITE,
                        ),
                        rx.text("Válido todos los martes. Aplican condiciones.", color=GRAY_MUTED, font_size="14px"),
                        rx.link(
                            rx.button(
                                "Aprovechar oferta",
                                background=RED_CINE,
                                color=WHITE,
                                border="none",
                                border_radius="8px",
                                padding="12px 28px",
                                font_size="15px",
                                font_weight="700",
                                cursor="pointer",
                                _hover={"background": RED_HOVER},
                            ),
                            href="/catalogo",
                            text_decoration="none",
                        ),
                        align_items="start",
                        spacing="3",
                    ),
                    max_width="1200px",
                    margin="0 auto",
                    padding="4rem 2rem",
                ),
                id="promo",
                background=f"linear-gradient(135deg, {GRAY_DARK} 0%, rgba(229,9,20,0.08) 100%)",
                border_top="1px solid rgba(229,9,20,0.15)",
                border_bottom="1px solid rgba(229,9,20,0.15)",
            ),

            background=BLACK_CINEMA,
            min_height="100vh",
        ),

        footer(),
        toast(),
        background=BLACK_CINEMA,
        font_family=FONT_BODY,
    )


def _movie_card_carousel(movie: dict) -> rx.Component:
    """Mini card para el carrusel horizontal del index."""
    from cinemax.components.movie_card import movie_card
    return rx.box(
        movie_card(movie),
        min_width="200px",
        max_width="220px",
    )

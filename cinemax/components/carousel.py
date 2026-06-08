"""
components/carousel.py
Carrusel horizontal de películas con scroll suave.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.components.movie_card import movie_card


def section_header(title: str, subtitle: str = "", link: str = "") -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(title, font_family=FONT_HEADING, font_size="2rem", color=WHITE, letter_spacing="1"),
            rx.box(width="48px", height="4px", background=RED_CINE, border_radius="2px"),
            rx.cond(
                subtitle != "",
                rx.text(subtitle, color=GRAY_MUTED, font_size="14px"),
            ),
            align_items="start",
            spacing="2",
        ),
        rx.cond(
            link != "",
            rx.link(
                rx.hstack(
                    rx.text("Ver todo", color=GRAY_MUTED, font_size="14px"),
                    rx.icon("arrow-right", size=14, color=GRAY_MUTED),
                    spacing="2",
                    align="center",
                ),
                href=link,
                text_decoration="none",
                color=GRAY_MUTED,
                _hover={"color": WHITE},
            ),
        ),
        justify="between",
        align="end",
        width="100%",
        margin_bottom="1.5rem",
    )


def movie_carousel(title: str, movies: list, subtitle: str = "") -> rx.Component:
    return rx.box(
        rx.box(
            section_header(title, subtitle, "/catalogo"),
            rx.box(
                rx.hstack(
                    rx.foreach(movies, movie_card),
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
    )

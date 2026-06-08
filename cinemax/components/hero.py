"""
components/hero.py
Hero section cinematográfico.
"""

import reflex as rx
from cinemax.pages.styles.theme import *


HERO_MOVIE = {
    "id": "1",
    "nombre": "Dune: Parte Dos",
    "descripcion": "Paul Atreides se une a los Fremen en una guerra de venganza contra los conspiradores que destruyeron a su familia. Una épica visual sin precedentes.",
    "categoria": "Ciencia Ficción",
    "duracion": "166 min",
    "clasificacion": "PG-13",
    "banner": "https://image.tmdb.org/t/p/original/xOMo8BRK7PfcJv9JCnx7s5hj0PX.jpg",
}


def hero_section() -> rx.Component:
    return rx.box(
        rx.image(
            src=HERO_MOVIE["banner"],
            position="absolute",
            top="0", left="0",
            width="100%", height="100%",
            object_fit="cover",
            object_position="center top",
            z_index="0",
        ),
        rx.box(
            position="absolute", top="0", left="0", right="0", bottom="0",
            background="linear-gradient(to right, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.4) 60%, rgba(0,0,0,0.1) 100%)",
            z_index="1",
        ),
        rx.box(
            position="absolute", bottom="0", left="0", right="0", height="40%",
            background=f"linear-gradient(0deg, {BLACK_CINEMA} 0%, transparent 100%)",
            z_index="1",
        ),

        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        "⭐ DESTACADO HOY",
                        background=f"linear-gradient(135deg, {GOLD_VIP}, {GOLD_DARK})",
                        color="#1a1200",
                        font_size="11px",
                        font_weight="800",
                        padding="4px 14px",
                        border_radius="20px",
                        letter_spacing="1",
                    ),
                    rx.box(
                        HERO_MOVIE["clasificacion"],
                        background="rgba(0,0,0,0.6)",
                        color=WHITE,
                        font_size="12px",
                        font_weight="700",
                        padding="4px 10px",
                        border_radius="4px",
                        border="1px solid rgba(255,255,255,0.3)",
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.text(
                    HERO_MOVIE["nombre"],
                    font_family=FONT_HEADING,
                    font_size=["3rem", "4rem", "5.5rem"],
                    color=WHITE,
                    letter_spacing="1",
                    line_height="1",
                    text_shadow="0 4px 24px rgba(0,0,0,0.8)",
                    max_width="700px",
                ),
                rx.hstack(
                    rx.hstack(
                        rx.icon("clock", size=14, color=WHITE_MUTED),
                        rx.text(HERO_MOVIE["duracion"], color=WHITE_MUTED, font_size="14px"),
                        spacing="2", align="center",
                    ),
                    rx.text("•", color=GRAY_MUTED),
                    rx.text(HERO_MOVIE["categoria"], color=WHITE_MUTED, font_size="14px"),
                    spacing="3",
                    align="center",
                ),
                rx.text(
                    HERO_MOVIE["descripcion"],
                    color="rgba(255,255,255,0.75)",
                    font_size="15px",
                    max_width="560px",
                    line_height="1.7",
                    display=["none", "block", "block"],
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon("play", size=16),
                                rx.text("Visualizar"),
                                spacing="2",
                                align="center",
                            ),
                            background=RED_CINE,
                            color=WHITE,
                            border="none",
                            border_radius="10px",
                            padding="14px 28px",
                            font_size="15px",
                            font_weight="700",
                            cursor="pointer",
                            transition="all 0.2s ease",
                            _hover={"background": RED_HOVER, "transform": "translateY(-2px)", "box_shadow": "0 8px 24px rgba(229,9,20,0.5)"},
                        ),
                        href=f"/pelicula/{HERO_MOVIE['id']}",
                        text_decoration="none",
                    ),
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon("info", size=16),
                                rx.text("Más info"),
                                spacing="2",
                                align="center",
                            ),
                            background="rgba(255,255,255,0.12)",
                            color=WHITE,
                            border="1px solid rgba(255,255,255,0.3)",
                            border_radius="10px",
                            padding="14px 28px",
                            font_size="15px",
                            font_weight="600",
                            cursor="pointer",
                            backdrop_filter="blur(8px)",
                            transition="all 0.2s ease",
                            _hover={"background": "rgba(255,255,255,0.2)"},
                        ),
                        href=f"/pelicula/{HERO_MOVIE['id']}",
                        text_decoration="none",
                    ),
                    spacing="4",
                    flex_wrap="wrap",
                ),
                spacing="5",
                align_items="start",
                max_width="700px",
            ),
            position="relative",
            z_index="2",
            padding=["4rem 1.5rem 4rem", "5rem 2.5rem 5rem", "6rem 4rem 5rem"],
            padding_top=["7rem", "8rem", "9rem"],
        ),

        position="relative",
        width="100%",
        min_height=["80vh", "88vh", "92vh"],
        overflow="hidden",
        display="flex",
        align_items="end",
    )

"""
components/movie_card.py
Card premium cinematográfica para cada película.
"""

import reflex as rx
from cinemax.pages.styles.theme import *


def movie_card(movie: dict) -> rx.Component:
    return rx.box(
        # Poster
        rx.box(
            rx.image(
                src=movie["imagen"],
                width="100%",
                height="340px",
                object_fit="cover",
                transition="transform 0.4s ease",
            ),
            # VIP Badge
            rx.cond(
                movie["vip"],
                rx.box(
                    "⭐ VIP",
                    position="absolute",
                    top="12px",
                    left="12px",
                    background=f"linear-gradient(135deg, {GOLD_VIP}, {GOLD_DARK})",
                    color="#1a1200",
                    font_size="11px",
                    font_weight="800",
                    padding="3px 10px",
                    border_radius="20px",
                    text_transform="uppercase",
                    letter_spacing="1",
                    z_index="2",
                ),
            ),
            # Clasificación
            rx.box(
                movie["clasificacion"],
                position="absolute",
                top="12px",
                right="12px",
                background="rgba(0,0,0,0.7)",
                color=WHITE,
                font_size="11px",
                font_weight="700",
                padding="3px 8px",
                border_radius="4px",
                border="1px solid rgba(255,255,255,0.2)",
                z_index="2",
            ),
            # Gradient overlay
            rx.box(
                position="absolute",
                bottom="0",
                left="0",
                right="0",
                height="60%",
                background="linear-gradient(0deg, rgba(0,0,0,0.95) 0%, transparent 100%)",
            ),
            position="relative",
            overflow="hidden",
        ),

        # Info
        rx.vstack(
            rx.text(
                movie["nombre"],
                color=WHITE,
                font_size="15px",
                font_weight="700",
                line_clamp="2",
                min_height="2.4em",
            ),
            rx.hstack(
                rx.box(
                    movie["categoria"],
                    background="rgba(229,9,20,0.15)",
                    color=RED_CINE,
                    font_size="11px",
                    padding="3px 10px",
                    border_radius="20px",
                    border=f"1px solid rgba(229,9,20,0.3)",
                ),
                rx.hstack(
                    rx.icon("clock", size=11, color=GRAY_MUTED),
                    rx.text(movie["duracion"], color=GRAY_MUTED, font_size="11px"),
                    spacing="1",
                    align="center",
                ),
                align="center",
                justify="between",
                width="100%",
            ),
            rx.hstack(
                rx.text(
                    "RD$ ", movie["precio"],
                    color=GOLD_VIP,
                    font_size="15px",
                    font_weight="700",
                ),
                rx.link(
                    rx.button(
                        "Ver horarios",
                        background=RED_CINE,
                        color=WHITE,
                        border="none",
                        border_radius="6px",
                        padding="7px 14px",
                        font_size="12px",
                        font_weight="600",
                        cursor="pointer",
                        transition="all 0.2s ease",
                        _hover={"background": RED_HOVER},
                    ),
                    href=f"/pelicula/{movie['id']}",
                    text_decoration="none",
                ),
                align="center",
                justify="between",
                width="100%",
            ),
            padding="14px",
            spacing="2",
            align_items="start",
        ),

        background=GRAY_DARK,
        border_radius="12px",
        overflow="hidden",
        cursor="pointer",
        transition="all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1)",
        position="relative",
        _hover={
            "transform": "translateY(-8px) scale(1.02)",
            "box_shadow": f"0 24px 60px rgba(0,0,0,0.8), 0 0 30px rgba(229,9,20,0.2)",
        },
        border="1px solid rgba(255,255,255,0.05)",
    )


def skeleton_card() -> rx.Component:
    return rx.box(
        rx.box(
            background="linear-gradient(90deg, #1a1a1a 25%, #2a2a2a 50%, #1a1a1a 75%)",
            height="340px",
            width="100%",
            animation="shimmer 1.5s infinite",
        ),
        rx.vstack(
            rx.box(background="#2a2a2a", height="16px", width="80%", border_radius="4px"),
            rx.box(background="#2a2a2a", height="12px", width="60%", border_radius="4px"),
            rx.box(background="#2a2a2a", height="12px", width="40%", border_radius="4px"),
            spacing="2",
            padding="14px",
            align_items="start",
        ),
        background=GRAY_DARK,
        border_radius="12px",
        overflow="hidden",
    )

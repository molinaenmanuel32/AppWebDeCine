"""
pages/pelicula.py
Página de detalle de película — layout cinematográfico.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.components.navbar import navbar
from cinemax.components.footer import footer
from cinemax.components.toast import toast
from cinemax.states.app_state import AppState


def showtime_button(time: str) -> rx.Component:
    """Botón de horario — itera sobre AppState.horarios (List[str])."""
    is_selected = AppState.selected_showtime == time
    return rx.button(
        time,
        on_click=AppState.set_showtime(time),
        background=rx.cond(is_selected, RED_CINE, "rgba(255,255,255,0.06)"),
        color=rx.cond(is_selected, WHITE, WHITE_MUTED),
        border=rx.cond(
            is_selected,
            f"1px solid {RED_CINE}",
            "1px solid rgba(255,255,255,0.1)",
        ),
        border_radius="8px",
        padding="10px 20px",
        font_size="14px",
        font_weight=rx.cond(is_selected, "700", "500"),
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={"background": rx.cond(is_selected, RED_HOVER, "rgba(255,255,255,0.12)")},
    )


@rx.page(route="/pelicula/[movie_id]", title="Película - CineMax", on_load=AppState.load_movie)
def movie_detail_page() -> rx.Component:
    return rx.box(
        navbar(),

        rx.box(
            rx.cond(
                AppState.movie_loaded,
                # ── Movie found ───────────────────────────────────────
                rx.box(
                    # Banner Hero
                    rx.box(
                        rx.image(
                            src=AppState.current_movie["banner"],
                            position="absolute",
                            top="0", left="0",
                            width="100%", height="100%",
                            object_fit="cover",
                            object_position="center top",
                        ),
                        rx.box(
                            position="absolute", top="0", left="0", right="0", bottom="0",
                            background="linear-gradient(0deg, rgba(15,15,15,1) 0%, rgba(15,15,15,0.3) 100%)",
                        ),
                        position="relative",
                        height=["250px", "380px", "500px"],
                        overflow="hidden",
                    ),

                    # Movie Content
                    rx.box(
                        rx.flex(
                            # Left — Poster
                            rx.box(
                                rx.image(
                                    src=AppState.current_movie["imagen"],
                                    width="100%",
                                    border_radius="12px",
                                    box_shadow="0 16px 48px rgba(0,0,0,0.8)",
                                    border="2px solid rgba(255,255,255,0.08)",
                                ),
                                min_width=["120px", "180px", "240px"],
                                max_width=["120px", "180px", "240px"],
                                margin_top=["-4rem", "-6rem", "-8rem"],
                                position="relative",
                                z_index="2",
                            ),

                            # Right — Details
                            rx.vstack(
                                # Title + VIP badge
                                rx.hstack(
                                    rx.text(
                                        AppState.current_movie["nombre"],
                                        font_family=FONT_HEADING,
                                        font_size=["2rem", "2.5rem", "3.5rem"],
                                        color=WHITE,
                                        letter_spacing="1",
                                        line_height="1.1",
                                    ),
                                    rx.cond(
                                        AppState.current_movie["vip"],
                                        rx.box(
                                            "⭐ VIP",
                                            background=f"linear-gradient(135deg, {GOLD_VIP}, {GOLD_DARK})",
                                            color="#1a1200",
                                            font_size="12px",
                                            font_weight="800",
                                            padding="4px 12px",
                                            border_radius="20px",
                                            white_space="nowrap",
                                        ),
                                    ),
                                    align="start",
                                    flex_wrap="wrap",
                                    gap="0.75rem",
                                ),

                                # Meta
                                rx.hstack(
                                    rx.box(
                                        AppState.current_movie["clasificacion"],
                                        background="rgba(255,255,255,0.1)",
                                        color=WHITE,
                                        padding="3px 10px",
                                        border_radius="6px",
                                        font_size="12px",
                                        font_weight="700",
                                    ),
                                    rx.box(
                                        AppState.current_movie["categoria"],
                                        background="rgba(229,9,20,0.15)",
                                        color=RED_CINE,
                                        padding="3px 12px",
                                        border_radius="20px",
                                        font_size="12px",
                                    ),
                                    rx.hstack(
                                        rx.icon("clock", size=13, color=GRAY_MUTED),
                                        rx.text(AppState.current_movie["duracion"], color=GRAY_MUTED, font_size="13px"),
                                        gap="0.3rem",
                                        align="center",
                                    ),
                                    spacing="2",
                                    flex_wrap="wrap",
                                    align="center",
                                ),

                                # Description
                                rx.text(
                                    AppState.current_movie["descripcion"],
                                    color="rgba(255,255,255,0.75)",
                                    font_size="15px",
                                    line_height="1.8",
                                    max_width="620px",
                                ),

                                # Price
                                rx.hstack(
                                    rx.text("Precio:", color=GRAY_MUTED, font_size="14px"),
                                    rx.text(
                                        "RD$ ",
                                        AppState.current_movie["precio"],
                                        color=GOLD_VIP,
                                        font_size="1.5rem",
                                        font_weight="700",
                                    ),
                                    spacing="2",
                                    align="center",
                                ),

                                # Showtimes — usa AppState.horarios (List[str])
                                rx.vstack(
                                    rx.text(
                                        "SELECCIONA HORARIO",
                                        color=WHITE_MUTED,
                                        font_size="11px",
                                        font_weight="700",
                                        letter_spacing="4",
                                    ),
                                    rx.box(
                                        rx.foreach(AppState.horarios, showtime_button),
                                        display="flex",
                                        flex_wrap="wrap",
                                        gap="0.6rem",
                                    ),
                                    align_items="start",
                                    spacing="3",
                                ),

                                # CTA
                                rx.link(
                                    rx.button(
                                        rx.hstack(
                                            rx.icon("ticket", size=18),
                                            rx.text("Reservar Entradas"),
                                            spacing="2",
                                            align="center",
                                        ),
                                        background=RED_CINE,
                                        color=WHITE,
                                        border="none",
                                        border_radius="10px",
                                        padding="14px 32px",
                                        font_size="16px",
                                        font_weight="700",
                                        cursor="pointer",
                                        transition="all 0.2s ease",
                                        _hover={
                                            "background": RED_HOVER,
                                            "transform": "translateY(-2px)",
                                            "box_shadow": "0 8px 24px rgba(229,9,20,0.5)",
                                        },
                                    ),
                                    href="/reservas",
                                    text_decoration="none",
                                ),

                                align_items="start",
                                spacing="5",
                                flex="1",
                            ),

                            gap="2.5rem",
                            flex_wrap="wrap",
                            align_items="start",
                        ),

                        # Trailer Section
                        rx.box(
                            rx.text(
                                "TRAILER OFICIAL",
                                font_family=FONT_HEADING,
                                font_size="1.5rem",
                                color=WHITE,
                                letter_spacing="3",
                                margin_bottom="1rem",
                            ),
                            rx.box(
                                    rx.el.iframe(
                                    src=AppState.current_movie["trailer"],
                                    width="100%",
                                    height="70vh",
                                    allow_fullscreen=True,
                                ),
                                
                                
                                border_radius="12px",
                                overflow="hidden",
                            ),
                            margin_top="3rem",
                        ),

                        max_width="1200px",
                        margin="0 auto",
                        padding=["1.5rem", "2rem", "3rem 4rem"],
                    ),

                    background=BLACK_CINEMA,
                    min_height="100vh",
                ),

                # ── Movie not found ───────────────────────────────────
                rx.box(
                    rx.vstack(
                        rx.icon("film", size=64, color=GRAY_MUTED),
                        rx.text(
                            "Película no encontrada",
                            font_family=FONT_HEADING,
                            font_size="2.5rem",
                            color=WHITE,
                        ),
                        rx.text(
                            "La película que buscas no existe o fue removida.",
                            color=GRAY_MUTED,
                            font_size="16px",
                        ),
                        rx.link(
                            rx.button(
                                "Volver al catálogo",
                                background=RED_CINE,
                                color=WHITE,
                                border="none",
                                border_radius="8px",
                                padding="12px 28px",
                                font_size="15px",
                                font_weight="600",
                                cursor="pointer",
                                _hover={"background": RED_HOVER},
                            ),
                            href="/catalogo",
                            text_decoration="none",
                        ),
                        align_items="center",
                        spacing="4",
                        padding="10rem 2rem",
                    ),
                    min_height="80vh",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
            ),
            background=BLACK_CINEMA,
            min_height="100vh",
        ),

        footer(),
        toast(),
        font_family=FONT_BODY,
        background=BLACK_CINEMA,
    )

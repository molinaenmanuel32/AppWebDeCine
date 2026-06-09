"""
components/vip_section.py
Sección exclusiva VIP con efectos premium.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.states.app_state import AppState


def vip_perk(icon: str, title: str, desc: str) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.icon(icon, size=28, color=GOLD_VIP),
            background="rgba(245,197,24,0.1)",
            padding="1rem",
            border_radius="12px",
            border=f"1px solid rgba(245,197,24,0.2)",
        ),
        rx.text(title, color=WHITE, font_size="15px", font_weight="700"),
        rx.text(desc, color=GRAY_MUTED, font_size="13px", text_align="center", max_width="200px"),
        align_items="center",
        spacing="3",
        padding="1.5rem",
        background="rgba(255,255,255,0.03)",
        border_radius="16px",
        border="1px solid rgba(245,197,24,0.1)",
        flex="1",
        min_width="180px",
    )


def vip_section() -> rx.Component:
    return rx.box(
        rx.box(
            rx.box(
                position="absolute",
                top="-100px",
                left="50%",
                transform="translateX(-50%)",
                width="600px",
                height="600px",
                background="radial-gradient(circle, rgba(245,197,24,0.06) 0%, transparent 70%)",
                pointer_events="none",
            ),

            rx.vstack(
                rx.vstack(
                    rx.hstack(
                        rx.icon("star", size=18, color=GOLD_VIP),
                        rx.text("EXPERIENCIA EXCLUSIVA", color=GOLD_VIP, font_size="12px", font_weight="800", letter_spacing="1"),
                        rx.icon("star", size=18, color=GOLD_VIP),
                        spacing="3",
                        align="center",
                    ),
                    rx.text(
                        "ACCESO VIP PREMIUM",
                        font_family=FONT_HEADING,
                        font_size=["2.5rem", "3.5rem", "4rem"],
                        color=WHITE,
                        letter_spacing="1",
                        text_align="center",
                    ),
                    rx.box(
                        width="80px",
                        height="4px",
                        background=f"linear-gradient(90deg, {GOLD_DARK}, {GOLD_VIP})",
                        border_radius="2px",
                    ),
                    rx.text(
                        "La mejor experiencia VIP. Salas exclusivas premium con tecnología de última generación.",
                        color=GRAY_MUTED,
                        font_size="16px",
                        text_align="center",
                        max_width="560px",
                        line_height="1.7",
                    ),
                    align_items="center",
                    spacing="4",
                    margin_bottom="3rem",
                ),

                rx.flex(
                    vip_perk("armchair", "Butacas Reclinables", "Asientos premium de cuero con reclinación total"),
                    vip_perk("tv", "4K Dolby Vision", "La imagen más nítida y brillante disponible"),
                    vip_perk("music", "Dolby Atmos", "Sonido envolvente que te sumerge en la película"),
                    vip_perk("wine", "Servicio en sala", "Comida y bebidas gourmet entregadas en tu asiento"),
                    gap="1.5rem",
                    flex_wrap="wrap",
                    justify_content="center",
                    width="100%",
                ),

                rx.hstack(
                    rx.link(
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("star", size=15, color=GOLD_VIP),
                            rx.text("Ver películas VIP"),
                            spacing="2",
                            align="center",
                        ),
                        on_click=AppState.go_to_vip_catalog,
                        background="transparent",
                        color=GOLD_VIP,
                        border=f"2px solid {GOLD_VIP}",
                        border_radius="10px",
                        padding="14px 32px",
                        font_size="15px",
                        font_weight="600",
                        cursor="pointer",
                        transition="all 0.2s ease",
                        _hover={"background": "rgba(245,197,24,0.1)", "transform": "translateY(-1px)"},
                    ),
                    spacing="4",
                    flex_wrap="wrap",
                    justify_content="center",
                    margin_top="2rem",
                ),

                align_items="center",
                spacing="0",
                position="relative",
                z_index="1",
            ),

            max_width="1200px",
            margin="0 auto",
            padding="5rem 2rem",
            position="relative",
        ),

        id="vip",
        background=f"linear-gradient(180deg, {BLACK_CINEMA} 0%, rgba(20,15,5,1) 50%, {BLACK_CINEMA} 100%)",
        border_top=f"1px solid rgba(245,197,24,0.1)",
        border_bottom=f"1px solid rgba(245,197,24,0.1)",
        width="100%",
        overflow="hidden",
        position="relative",
    )

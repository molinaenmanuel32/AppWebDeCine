"""
pages/mis_reservas.py
Historial de reservas del usuario autenticado — KankyCine.
Sistema de estados: confirmed / used / expired / cancelled.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.components.navbar import navbar
from cinemax.components.footer import footer
from cinemax.components.toast import toast
from cinemax.states.app_state import AppState


# ─── CONSTANTES DE COLOR POR ESTADO ──────────────────────────────────────────
# Usadas en múltiples lugares; definidas aquí para consistencia visual.
STATUS_CONFIRMED_COLOR  = "#00c07f"
STATUS_CONFIRMED_BG     = "rgba(0,192,127,0.10)"
STATUS_CONFIRMED_BORDER = "rgba(0,192,127,0.25)"

STATUS_USED_COLOR       = "#888888"
STATUS_USED_BG          = "rgba(136,136,136,0.10)"
STATUS_USED_BORDER      = "rgba(136,136,136,0.25)"

STATUS_EXPIRED_COLOR    = "#f5a623"
STATUS_EXPIRED_BG       = "rgba(245,166,35,0.10)"
STATUS_EXPIRED_BORDER   = "rgba(245,166,35,0.25)"

STATUS_CANCELLED_COLOR  = "#e50914"
STATUS_CANCELLED_BG     = "rgba(229,9,20,0.10)"
STATUS_CANCELLED_BORDER = "rgba(229,9,20,0.25)"


# ─── QR SVG ───────────────────────────────────────────────────────────────────

def qr_svg_small() -> rx.Component:
    return rx.html("""
    <svg width="90" height="90" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
      <rect width="120" height="120" fill="#1a1a1a" rx="8"/>
      <rect x="10" y="10" width="30" height="30" fill="none" stroke="#e50914" stroke-width="3" rx="2"/>
      <rect x="17" y="17" width="16" height="16" fill="#e50914" rx="1"/>
      <rect x="80" y="10" width="30" height="30" fill="none" stroke="#e50914" stroke-width="3" rx="2"/>
      <rect x="87" y="17" width="16" height="16" fill="#e50914" rx="1"/>
      <rect x="10" y="80" width="30" height="30" fill="none" stroke="#e50914" stroke-width="3" rx="2"/>
      <rect x="17" y="87" width="16" height="16" fill="#e50914" rx="1"/>
      <rect x="50" y="10" width="6" height="6" fill="white" rx="1"/>
      <rect x="60" y="10" width="6" height="6" fill="white" rx="1"/>
      <rect x="50" y="20" width="6" height="6" fill="white" rx="1"/>
      <rect x="70" y="20" width="6" height="6" fill="white" rx="1"/>
      <rect x="50" y="30" width="6" height="6" fill="white" rx="1"/>
      <rect x="60" y="30" width="6" height="6" fill="white" rx="1"/>
      <rect x="10" y="50" width="6" height="6" fill="white" rx="1"/>
      <rect x="20" y="50" width="6" height="6" fill="white" rx="1"/>
      <rect x="30" y="60" width="6" height="6" fill="white" rx="1"/>
      <rect x="10" y="70" width="6" height="6" fill="white" rx="1"/>
      <rect x="50" y="50" width="6" height="6" fill="white" rx="1"/>
      <rect x="60" y="50" width="6" height="6" fill="white" rx="1"/>
      <rect x="70" y="50" width="6" height="6" fill="white" rx="1"/>
      <rect x="80" y="50" width="6" height="6" fill="white" rx="1"/>
      <rect x="50" y="60" width="6" height="6" fill="white" rx="1"/>
      <rect x="80" y="60" width="6" height="6" fill="white" rx="1"/>
      <rect x="60" y="70" width="6" height="6" fill="white" rx="1"/>
      <rect x="80" y="70" width="6" height="6" fill="white" rx="1"/>
      <rect x="50" y="80" width="6" height="6" fill="white" rx="1"/>
      <rect x="70" y="80" width="6" height="6" fill="white" rx="1"/>
      <rect x="90" y="80" width="6" height="6" fill="white" rx="1"/>
      <rect x="100" y="90" width="6" height="6" fill="white" rx="1"/>
    </svg>
    """)


# ─── BADGE DE ESTADO ──────────────────────────────────────────────────────────
# Recibe el campo status del booking (ObjectVar dentro de foreach).

def status_badge_reactive(status) -> rx.Component:
    """Badge que reacciona al valor de status del booking."""
    return rx.box(
        # confirmed
        rx.cond(
            status == "confirmed",
            rx.hstack(
                rx.box(width="7px", height="7px", border_radius="50%",
                       background=STATUS_CONFIRMED_COLOR, flex_shrink="0"),
                rx.text("Confirmado", font_size="11px", font_weight="700",
                        color=STATUS_CONFIRMED_COLOR, letter_spacing="0.5px"),
                spacing="2", align="center",
            ),
            rx.box(),
        ),
        # used
        rx.cond(
            status == "used",
            rx.hstack(
                rx.box(width="7px", height="7px", border_radius="50%",
                       background=STATUS_USED_COLOR, flex_shrink="0"),
                rx.text("Utilizado", font_size="11px", font_weight="700",
                        color=STATUS_USED_COLOR, letter_spacing="0.5px"),
                spacing="2", align="center",
            ),
            rx.box(),
        ),
        # expired
        rx.cond(
            status == "expired",
            rx.hstack(
                rx.box(width="7px", height="7px", border_radius="50%",
                       background=STATUS_EXPIRED_COLOR, flex_shrink="0"),
                rx.text("Expirado", font_size="11px", font_weight="700",
                        color=STATUS_EXPIRED_COLOR, letter_spacing="0.5px"),
                spacing="2", align="center",
            ),
            rx.box(),
        ),
        # cancelled
        rx.cond(
            status == "cancelled",
            rx.hstack(
                rx.box(width="7px", height="7px", border_radius="50%",
                       background=STATUS_CANCELLED_COLOR, flex_shrink="0"),
                rx.text("Cancelado", font_size="11px", font_weight="700",
                        color=STATUS_CANCELLED_COLOR, letter_spacing="0.5px"),
                spacing="2", align="center",
            ),
            rx.box(),
        ),
        padding="4px 10px",
        background=rx.cond(
            status == "confirmed", STATUS_CONFIRMED_BG,
            rx.cond(
                status == "used", STATUS_USED_BG,
                rx.cond(
                    status == "expired", STATUS_EXPIRED_BG,
                    STATUS_CANCELLED_BG,
                ),
            ),
        ),
        border=rx.cond(
            status == "confirmed", f"1px solid {STATUS_CONFIRMED_BORDER}",
            rx.cond(
                status == "used", f"1px solid {STATUS_USED_BORDER}",
                rx.cond(
                    status == "expired", f"1px solid {STATUS_EXPIRED_BORDER}",
                    f"1px solid {STATUS_CANCELLED_BORDER}",
                ),
            ),
        ),
        border_radius="20px",
        display="inline-flex",
    )


# ─── BANNER "TICKET UTILIZADO" en la tarjeta ─────────────────────────────────

def used_banner_card(booking) -> rx.Component:
    """Franja que aparece en la tarjeta cuando status == 'used'."""
    return rx.cond(
        booking["status"] == "used",
        rx.box(
            rx.hstack(
                rx.icon("check-circle-2", size=15, color=STATUS_USED_COLOR),
                rx.text(
                    "✓ Ticket utilizado",
                    color=STATUS_USED_COLOR,
                    font_size="12px",
                    font_weight="700",
                    letter_spacing="0.5px",
                ),
                rx.cond(
                    booking["validated_at"] != "",
                    rx.text(
                        "· ", booking["validated_at"],
                        color=GRAY_MUTED,
                        font_size="11px",
                    ),
                    rx.box(),
                ),
                spacing="2",
                align="center",
            ),
            padding="8px 14px",
            background=STATUS_USED_BG,
            border="1px solid rgba(136,136,136,0.2)",
            border_radius="8px",
            width="100%",
        ),
        rx.box(),
    )


# ─── TARJETA DE RESERVA ───────────────────────────────────────────────────────

def booking_card(booking: dict, index: int) -> rx.Component:
    is_used = booking["status"] == "used"
    is_cancelled = booking["status"] == "cancelled"
    is_inactive = is_used | is_cancelled

    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.icon("ticket", size=18,
                                color=rx.cond(is_inactive, GRAY_MUTED, RED_CINE)),
                        width="40px",
                        height="40px",
                        background=rx.cond(
                            is_inactive,
                            "rgba(136,136,136,0.08)",
                            "rgba(229,9,20,0.10)",
                        ),
                        border=rx.cond(
                            is_inactive,
                            "1px solid rgba(136,136,136,0.15)",
                            "1px solid rgba(229,9,20,0.20)",
                        ),
                        border_radius="10px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        flex_shrink="0",
                    ),
                    rx.vstack(
                        rx.text(
                            booking["movie"],
                            color=rx.cond(is_inactive, WHITE_MUTED, WHITE),
                            font_size="17px",
                            font_weight="700",
                            line_height="1.2",
                        ),
                        rx.text(
                            booking["code"],
                            color=GRAY_MUTED,
                            font_size="11px",
                            font_weight="600",
                            letter_spacing="0.5px",
                            font_family=FONT_MONO,
                        ),
                        align_items="start",
                        spacing="1",
                    ),
                    spacing="3",
                    align="center",
                    flex="1",
                ),
                status_badge_reactive(booking["status"]),
                justify="between",
                align="center",
                width="100%",
                flex_wrap="wrap",
                gap="0.5rem",
            ),

            # Banner "ticket utilizado"
            used_banner_card(booking),

            # Divisor
            rx.box(width="100%", height="1px",
                   background="rgba(255,255,255,0.06)"),

            # Detalles flex-wrap
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("calendar", size=13, color=GRAY_MUTED),
                        rx.text("FECHA", color=GRAY_MUTED, font_size="10px",
                                font_weight="700", letter_spacing="1.5px"),
                        spacing="1", align="center",
                    ),
                    rx.text(booking["date"],
                            color=rx.cond(is_inactive, GRAY_MUTED, WHITE_SOFT),
                            font_size="14px", font_weight="600"),
                    align_items="start", spacing="1",
                    min_width="120px", flex="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.icon("clock", size=13, color=GRAY_MUTED),
                        rx.text("HORARIO", color=GRAY_MUTED, font_size="10px",
                                font_weight="700", letter_spacing="1.5px"),
                        spacing="1", align="center",
                    ),
                    rx.text(booking["time"],
                            color=rx.cond(is_inactive, GRAY_MUTED, WHITE_SOFT),
                            font_size="14px", font_weight="600"),
                    align_items="start", spacing="1",
                    min_width="120px", flex="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.icon("tv-2", size=13, color=GRAY_MUTED),
                        rx.text("SALA", color=GRAY_MUTED, font_size="10px",
                                font_weight="700", letter_spacing="1.5px"),
                        spacing="1", align="center",
                    ),
                    rx.text(booking["hall"],
                            color=rx.cond(is_inactive, GRAY_MUTED, WHITE_SOFT),
                            font_size="14px", font_weight="600"),
                    align_items="start", spacing="1",
                    min_width="120px", flex="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.icon("map-pin", size=13, color=GRAY_MUTED),
                        rx.text("SUCURSAL", color=GRAY_MUTED, font_size="10px",
                                font_weight="700", letter_spacing="1.5px"),
                        spacing="1", align="center",
                    ),
                    rx.text(booking.get("branch", "—"),
                            color=rx.cond(is_inactive, GRAY_MUTED, GOLD_VIP),
                            font_size="14px", font_weight="600"),
                    align_items="start", spacing="1",
                    min_width="120px", flex="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.icon("users", size=13, color=GRAY_MUTED),
                        rx.text("BOLETOS", color=GRAY_MUTED, font_size="10px",
                                font_weight="700", letter_spacing="1.5px"),
                        spacing="1", align="center",
                    ),
                    rx.text(
                        booking["seat_count"],
                        rx.cond(
                            booking["seat_count"].to(int) > 1,
                            " boletos", " boleto",
                        ),
                        color=rx.cond(is_inactive, GRAY_MUTED, WHITE_SOFT),
                        font_size="14px", font_weight="600",
                    ),
                    align_items="start", spacing="1",
                    min_width="120px", flex="1",
                ),
                display="flex", flex_wrap="wrap", gap="1rem", width="100%",
            ),

            # Fila inferior: fecha compra + total
            rx.hstack(
                rx.vstack(
                    rx.text("FECHA DE COMPRA", color=GRAY_MUTED, font_size="10px",
                            font_weight="700", letter_spacing="1px"),
                    rx.text(booking["purchase_date"], color=WHITE_MUTED,
                            font_size="13px", font_weight="500"),
                    align_items="start", spacing="0",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text("TOTAL", color=GRAY_MUTED, font_size="10px",
                            font_weight="700", letter_spacing="1px"),
                    rx.text(
                        "RD$ ", booking["total"],
                        color=rx.cond(is_inactive, GRAY_MUTED, GOLD_VIP),
                        font_size="18px", font_weight="800",
                    ),
                    align_items="end", spacing="0",
                ),
                width="100%", align="end", flex_wrap="wrap", gap="0.75rem",
            ),

            # Botón ver ticket
            rx.button(
                rx.hstack(
                    rx.icon("qr-code", size=16),
                    rx.text("Ver Ticket"),
                    spacing="2", align="center",
                ),
                on_click=AppState.open_booking_ticket(index),
                background=rx.cond(is_inactive, "transparent", "transparent"),
                color=rx.cond(is_inactive, GRAY_MUTED, RED_CINE),
                border=rx.cond(
                    is_inactive,
                    "1px solid rgba(136,136,136,0.25)",
                    f"1px solid {RED_CINE}",
                ),
                border_radius="8px",
                padding="10px 20px",
                font_size="13px",
                font_weight="700",
                cursor="pointer",
                width="100%",
                transition="all 0.2s ease",
                _hover=rx.cond(
                    is_inactive,
                    {"background": "rgba(136,136,136,0.08)", "color": WHITE_MUTED},
                    {
                        "background": "rgba(229,9,20,0.1)",
                        "transform": "translateY(-1px)",
                        "box_shadow": "0 4px 16px rgba(229,9,20,0.2)",
                    },
                ),
            ),

            spacing="4",
            width="100%",
            padding="1.5rem",
        ),

        background=rx.cond(is_inactive, "rgba(20,20,20,0.8)", GRAY_DARK),
        border=rx.cond(
            is_inactive,
            "1px solid rgba(255,255,255,0.04)",
            "1px solid rgba(255,255,255,0.07)",
        ),
        border_radius="16px",
        opacity=rx.cond(is_inactive, "0.75", "1"),
        transition="all 0.25s ease",
        _hover={
            "border_color": rx.cond(
                is_inactive,
                "rgba(136,136,136,0.2)",
                "rgba(229,9,20,0.3)",
            ),
            "box_shadow": "0 8px 32px rgba(0,0,0,0.4)",
            "transform": "translateY(-2px)",
            "opacity": "1",
        },
        width="100%",
    )


# ─── ESTADO VACÍO ─────────────────────────────────────────────────────────────

def empty_state() -> rx.Component:
    return rx.vstack(
        rx.box(rx.text("🎟️", font_size="64px"),
               display="flex", justify_content="center"),
        rx.vstack(
            rx.text("Sin reservas aún", color=WHITE, font_size="24px",
                    font_weight="700", text_align="center",
                    font_family=FONT_HEADING),
            rx.text(
                "Todavía no has reservado ninguna película. ¡Explora la cartelera y compra tus boletos!",
                color=GRAY_MUTED, font_size="15px", text_align="center",
                max_width="400px", line_height="1.7",
            ),
            align_items="center", spacing="3",
        ),
        rx.link(
            rx.button(
                rx.hstack(
                    rx.icon("clapperboard", size=18),
                    rx.text("Ver Cartelera"),
                    spacing="2", align="center",
                ),
                background=RED_CINE, color=WHITE, border="none",
                border_radius="10px", padding="14px 32px",
                font_size="15px", font_weight="700", cursor="pointer",
                transition="all 0.2s ease",
                _hover={"background": RED_HOVER, "transform": "translateY(-2px)",
                        "box_shadow": "0 8px 24px rgba(229,9,20,0.4)"},
            ),
            href="/catalogo", text_decoration="none",
        ),
        align_items="center", spacing="6", padding="5rem 2rem",
        background="rgba(255,255,255,0.02)",
        border="1px dashed rgba(255,255,255,0.1)",
        border_radius="20px", width="100%",
    )


# ─── TICKET MODAL ─────────────────────────────────────────────────────────────

def ticket_status_header() -> rx.Component:
    """Header del modal que varía según el estado del ticket abierto."""
    return rx.cond(
        AppState.ticket_status == "used",
        # ── USADO: franja gris con sello ──────────────────────────────
        rx.vstack(
            rx.hstack(
                rx.text("🎬", font_size="28px"),
                rx.vstack(
                    rx.text("KANKYCINE", color=GRAY_MUTED, font_size="22px",
                            font_weight="900", letter_spacing="4"),
                    rx.text("ENTERTAINMENT", color=GRAY_MUTED,
                            font_size="9px", letter_spacing="6"),
                    spacing="0", align_items="start",
                ),
                spacing="3", align="center",
            ),
            rx.box(width="100%", height="2px",
                   background="linear-gradient(90deg, transparent, #888, transparent)"),
            # Sello "TICKET UTILIZADO"
            rx.box(
                rx.hstack(
                    rx.icon("check-circle-2", size=16, color=STATUS_USED_COLOR),
                    rx.text("TICKET UTILIZADO", color=STATUS_USED_COLOR,
                            font_size="13px", font_weight="800",
                            letter_spacing="2px"),
                    spacing="2", align="center",
                ),
                padding="8px 20px",
                background=STATUS_USED_BG,
                border=f"1px solid {STATUS_USED_BORDER}",
                border_radius="20px",
            ),
            rx.cond(
                AppState.ticket_validated_at != "",
                rx.text(
                    "Validado: ", AppState.ticket_validated_at,
                    color=GRAY_MUTED, font_size="11px",
                ),
                rx.box(),
            ),
            align_items="center", spacing="3",
            padding="1.5rem 1.5rem 1rem",
            background="linear-gradient(180deg, rgba(136,136,136,0.06) 0%, transparent 100%)",
            width="100%", border_radius="20px 20px 0 0",
        ),
        # ── DEFAULT: header rojo normal ───────────────────────────────
        rx.cond(
            AppState.ticket_status == "cancelled",
            rx.vstack(
                rx.hstack(
                    rx.text("🎬", font_size="28px"),
                    rx.vstack(
                        rx.text("KANKYCINE", color=RED_CINE, font_size="22px",
                                font_weight="900", letter_spacing="4"),
                        rx.text("ENTERTAINMENT", color=GRAY_MUTED,
                                font_size="9px", letter_spacing="6"),
                        spacing="0", align_items="start",
                    ),
                    spacing="3", align="center",
                ),
                rx.box(width="100%", height="2px",
                       background=f"linear-gradient(90deg, transparent, {RED_CINE}, transparent)"),
                rx.box(
                    rx.hstack(
                        rx.icon("x-circle", size=14, color=STATUS_CANCELLED_COLOR),
                        rx.text("RESERVA CANCELADA", color=STATUS_CANCELLED_COLOR,
                                font_size="13px", font_weight="700", letter_spacing="2"),
                        spacing="2", align="center",
                    ),
                    padding="6px 16px",
                    background=STATUS_CANCELLED_BG,
                    border=f"1px solid {STATUS_CANCELLED_BORDER}",
                    border_radius="20px",
                ),
                align_items="center", spacing="3",
                padding="1.5rem 1.5rem 1rem",
                background="linear-gradient(180deg, rgba(229,9,20,0.06) 0%, transparent 100%)",
                width="100%", border_radius="20px 20px 0 0",
            ),
            rx.cond(
                AppState.ticket_status == "expired",
                rx.vstack(
                    rx.hstack(
                        rx.text("🎬", font_size="28px"),
                        rx.vstack(
                            rx.text("KANKYCINE", color=RED_CINE, font_size="22px",
                                    font_weight="900", letter_spacing="4"),
                            rx.text("ENTERTAINMENT", color=GRAY_MUTED,
                                    font_size="9px", letter_spacing="6"),
                            spacing="0", align_items="start",
                        ),
                        spacing="3", align="center",
                    ),
                    rx.box(width="100%", height="2px",
                           background=f"linear-gradient(90deg, transparent, {RED_CINE}, transparent)"),
                    rx.box(
                        rx.hstack(
                            rx.icon("clock-x", size=14, color=STATUS_EXPIRED_COLOR),
                            rx.text("TICKET EXPIRADO", color=STATUS_EXPIRED_COLOR,
                                    font_size="13px", font_weight="700", letter_spacing="2"),
                            spacing="2", align="center",
                        ),
                        padding="6px 16px",
                        background=STATUS_EXPIRED_BG,
                        border=f"1px solid {STATUS_EXPIRED_BORDER}",
                        border_radius="20px",
                    ),
                    align_items="center", spacing="3",
                    padding="1.5rem 1.5rem 1rem",
                    background="linear-gradient(180deg, rgba(245,166,35,0.06) 0%, transparent 100%)",
                    width="100%", border_radius="20px 20px 0 0",
                ),
                # confirmed (default)
                rx.vstack(
                    rx.hstack(
                        rx.text("🎬", font_size="28px"),
                        rx.vstack(
                            rx.text("KANKYCINE", color=RED_CINE, font_size="22px",
                                    font_weight="900", letter_spacing="4"),
                            rx.text("ENTERTAINMENT", color=GRAY_MUTED,
                                    font_size="9px", letter_spacing="6"),
                            spacing="0", align_items="start",
                        ),
                        spacing="3", align="center",
                    ),
                    rx.box(width="100%", height="2px",
                           background=f"linear-gradient(90deg, transparent, {RED_CINE}, transparent)"),
                    rx.text("✓ RESERVA CONFIRMADA", color=STATUS_CONFIRMED_COLOR,
                            font_size="13px", font_weight="700", letter_spacing="2"),
                    align_items="center", spacing="3",
                    padding="1.5rem 1.5rem 1rem",
                    background="linear-gradient(180deg, rgba(229,9,20,0.08) 0%, transparent 100%)",
                    width="100%", border_radius="20px 20px 0 0",
                ),
            ),
        ),
    )


def mis_reservas_ticket_modal() -> rx.Component:
    is_inactive = (AppState.ticket_status == "used") | (AppState.ticket_status == "cancelled")

    return rx.cond(
        AppState.mis_reservas_ticket_visible,
        rx.box(
            # Overlay
            rx.box(
                on_click=AppState.close_booking_ticket,
                position="fixed", top="0", left="0", right="0", bottom="0",
                background="rgba(0,0,0,0.85)", z_index="2000",
                backdrop_filter="blur(6px)",
            ),
            # Panel
            rx.box(
                rx.vstack(
                    # Header dinámico por estado
                    ticket_status_header(),

                    # Contenido
                    rx.vstack(
                        # Película
                        rx.vstack(
                            rx.text("PELÍCULA", color=GRAY_MUTED, font_size="10px",
                                    font_weight="700", letter_spacing="3"),
                            rx.text(AppState.ticket_movie, color=WHITE,
                                    font_size="18px", font_weight="800",
                                    text_align="center"),
                            align_items="center", spacing="1",
                        ),

                        rx.box(width="100%", height="1px",
                               background="repeating-linear-gradient(90deg, rgba(255,255,255,0.2) 0, rgba(255,255,255,0.2) 8px, transparent 8px, transparent 16px)",
                               margin="0.5rem 0"),

                        # Sala / Horario / Fecha
                        rx.grid(
                            rx.vstack(
                                rx.text("SALA", color=GRAY_MUTED, font_size="10px",
                                        font_weight="700", letter_spacing="2"),
                                rx.text(AppState.ticket_hall, color=WHITE,
                                        font_size="16px", font_weight="700"),
                                align_items="center", spacing="1",
                            ),
                            rx.vstack(
                                rx.text("HORARIO", color=GRAY_MUTED, font_size="10px",
                                        font_weight="700", letter_spacing="2"),
                                rx.text(AppState.ticket_showtime, color=WHITE,
                                        font_size="16px", font_weight="700"),
                                align_items="center", spacing="1",
                            ),
                            rx.vstack(
                                rx.text("FECHA", color=GRAY_MUTED, font_size="10px",
                                        font_weight="700", letter_spacing="2"),
                                rx.text(AppState.ticket_date, color=WHITE,
                                        font_size="13px", font_weight="600"),
                                align_items="center", spacing="1",
                            ),
                            columns="3", gap="1rem", width="100%",
                        ),

                        rx.box(width="100%", height="1px",
                               background="repeating-linear-gradient(90deg, rgba(255,255,255,0.2) 0, rgba(255,255,255,0.2) 8px, transparent 8px, transparent 16px)",
                               margin="0.25rem 0"),

                        # Sucursal
                        rx.vstack(
                            rx.text("SUCURSAL", color=GRAY_MUTED, font_size="10px",
                                    font_weight="700", letter_spacing="3"),
                            rx.hstack(
                                rx.icon("map-pin", size=14, color=GOLD_VIP),
                                rx.text(AppState.ticket_branch, color=GOLD_VIP,
                                        font_size="15px", font_weight="700"),
                                spacing="2",
                                align="center",
                            ),
                            align_items="center", spacing="1",
                        ),

                        rx.box(width="100%", height="1px",
                               background="repeating-linear-gradient(90deg, rgba(255,255,255,0.2) 0, rgba(255,255,255,0.2) 8px, transparent 8px, transparent 16px)",
                               margin="0.25rem 0"),

                        # Asientos
                        rx.vstack(
                            rx.text("ASIENTOS", color=GRAY_MUTED, font_size="10px",
                                    font_weight="700", letter_spacing="3"),
                            rx.box(
                                rx.foreach(
                                    AppState.ticket_seats,
                                    lambda s: rx.box(
                                        s,
                                        background=rx.cond(is_inactive, GRAY_LIGHT, RED_CINE),
                                        color=rx.cond(is_inactive, GRAY_MUTED, WHITE),
                                        font_size="12px", font_weight="700",
                                        padding="4px 10px", border_radius="6px",
                                    )
                                ),
                                display="flex", flex_wrap="wrap",
                                gap="0.5rem", justify_content="center",
                            ),
                            align_items="center", spacing="2",
                        ),

                        rx.box(width="100%", height="1px",
                               background="repeating-linear-gradient(90deg, rgba(255,255,255,0.2) 0, rgba(255,255,255,0.2) 8px, transparent 8px, transparent 16px)",
                               margin="0.25rem 0"),

                        # Método de pago + código
                        rx.hstack(
                            rx.vstack(
                                rx.text("MÉTODO DE PAGO", color=GRAY_MUTED, font_size="10px",
                                        font_weight="700", letter_spacing="2"),
                                rx.text(AppState.ticket_payment_method, color=WHITE_SOFT,
                                        font_size="13px", font_weight="600"),
                                align_items="start", spacing="1",
                            ),
                            rx.spacer(),
                            rx.vstack(
                                rx.text("CÓDIGO", color=GRAY_MUTED, font_size="10px",
                                        font_weight="700", letter_spacing="2"),
                                rx.text(AppState.ticket_code, color=WHITE_MUTED,
                                        font_size="10px", font_weight="600",
                                        font_family=FONT_MONO, letter_spacing="0.5px"),
                                align_items="end", spacing="1",
                            ),
                            width="100%", align="center",
                        ),

                        rx.box(width="100%", height="1px",
                               background="repeating-linear-gradient(90deg, rgba(255,255,255,0.2) 0, rgba(255,255,255,0.2) 8px, transparent 8px, transparent 16px)",
                               margin="0.25rem 0"),

                        # Total + QR
                        rx.hstack(
                            rx.vstack(
                                rx.text("TOTAL PAGADO", color=GRAY_MUTED, font_size="10px",
                                        font_weight="700", letter_spacing="2"),
                                rx.text(
                                    "RD$ ", AppState.ticket_total,
                                    color=rx.cond(is_inactive, GRAY_MUTED, GOLD_VIP),
                                    font_size="24px", font_weight="900",
                                ),
                                align_items="start", spacing="1",
                            ),
                            rx.spacer(),
                            rx.vstack(
                                qr_svg_small(),
                                rx.text(AppState.ticket_code, color=GRAY_MUTED,
                                        font_size="8px", font_weight="600",
                                        letter_spacing="1", text_align="center"),
                                align_items="center", spacing="1",
                            ),
                            width="100%", align="center",
                        ),

                        padding="1rem 1.5rem 1.5rem",
                        spacing="4",
                        width="100%",
                        opacity=rx.cond(is_inactive, "0.75", "1"),
                    ),

                    # Footer
                    rx.vstack(
                        rx.box(width="100%", height="1px",
                               background="rgba(255,255,255,0.08)"),
                        rx.cond(
                            AppState.ticket_status == "confirmed",
                            rx.text(
                                "Presenta este ticket en la entrada del cine. Válido solo para la función indicada.",
                                color=GRAY_MUTED, font_size="11px",
                                text_align="center", padding="0 1rem",
                            ),
                            rx.text(
                                "Este ticket ya no es válido para ingresar al cine.",
                                color=GRAY_MUTED, font_size="11px",
                                text_align="center", padding="0 1rem",
                            ),
                        ),
                        rx.button(
                            rx.hstack(rx.icon("x", size=16), rx.text("Cerrar"),
                                      spacing="2", align="center"),
                            on_click=AppState.close_booking_ticket,
                            background=rx.cond(is_inactive, GRAY_MID, RED_CINE),
                            color=WHITE, border="none", border_radius="10px",
                            padding="12px 32px", font_size="14px", font_weight="700",
                            cursor="pointer", width="100%", margin="0 1rem",
                            _hover={"background": rx.cond(is_inactive, GRAY_LIGHT, RED_HOVER)},
                        ),
                        spacing="3", padding="1rem 1rem 1.5rem",
                        align_items="center", width="100%",
                        background="rgba(255,255,255,0.02)",
                        border_radius="0 0 20px 20px",
                    ),

                    spacing="0", width="100%",
                ),
                position="fixed", top="50%", left="50%",
                transform="translate(-50%, -50%)",
                background=GRAY_DARK,
                border=rx.cond(
                    AppState.ticket_status == "used",
                    "1px solid rgba(136,136,136,0.2)",
                    "1px solid rgba(229,9,20,0.3)",
                ),
                border_radius="20px",
                width=["92vw", "440px"],
                max_height="92vh", overflow_y="auto",
                z_index="2001",
                box_shadow="0 40px 80px rgba(0,0,0,0.9)",
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            z_index="1999",
        ),
        rx.box(),
    )


# ─── STATS BAR ────────────────────────────────────────────────────────────────

def stats_bar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(AppState.booking_count, color=WHITE, font_size="28px",
                            font_weight="900", font_family=FONT_HEADING),
                    rx.text("Reservas totales", color=GRAY_MUTED, font_size="12px"),
                    align_items="center", spacing="0",
                ),
                rx.box(width="1px", height="40px", background="rgba(255,255,255,0.1)"),
                rx.vstack(
                    rx.text("🎬", font_size="28px"),
                    rx.text("KankyCine Member", color=GRAY_MUTED, font_size="12px"),
                    align_items="center", spacing="0",
                ),
                rx.box(width="1px", height="40px", background="rgba(255,255,255,0.1)"),
                rx.vstack(
                    rx.hstack(
                        rx.box(width="10px", height="10px", border_radius="50%",
                               background="#00c07f",
                               box_shadow="0 0 8px rgba(0,192,127,0.6)"),
                        rx.text("Activa", color="#00c07f", font_size="16px",
                                font_weight="700"),
                        spacing="2", align="center",
                    ),
                    rx.text("Estado de cuenta", color=GRAY_MUTED, font_size="12px"),
                    align_items="center", spacing="0",
                ),
                spacing="6", justify="center", flex_wrap="wrap", gap="1.5rem",
            ),
            # Botón de simulación API — quitar en producción real
            rx.button(
                rx.hstack(
                    rx.icon("refresh-cw", size=13),
                    rx.text("Simular estados desde API", font_size="12px"),
                    spacing="2", align="center",
                ),
                on_click=AppState.simulate_booking_statuses,
                background="transparent",
                color=GRAY_MUTED,
                border="1px dashed rgba(255,255,255,0.15)",
                border_radius="8px",
                padding="6px 14px",
                cursor="pointer",
                font_size="12px",
                transition="all 0.2s ease",
                _hover={"color": WHITE_SOFT,
                        "border_color": "rgba(255,255,255,0.35)"},
            ),
            align_items="center", spacing="3", width="100%",
        ),
        padding="1.5rem 2rem",
        background="rgba(255,255,255,0.02)",
        border="1px solid rgba(255,255,255,0.07)",
        border_radius="16px", width="100%",
    )


# ─── LEYENDA DE ESTADOS ───────────────────────────────────────────────────────

def status_legend() -> rx.Component:
    def legend_item(dot_color: str, label: str) -> rx.Component:
        return rx.hstack(
            rx.box(width="8px", height="8px", border_radius="50%",
                   background=dot_color, flex_shrink="0"),
            rx.text(label, color=GRAY_MUTED, font_size="12px"),
            spacing="2", align="center",
        )

    return rx.hstack(
        legend_item(STATUS_CONFIRMED_COLOR, "Confirmado"),
        legend_item(STATUS_USED_COLOR, "Utilizado"),
        legend_item(STATUS_EXPIRED_COLOR, "Expirado"),
        legend_item(STATUS_CANCELLED_COLOR, "Cancelado"),
        spacing="5",
        flex_wrap="wrap",
        gap="0.5rem",
    )


# ─── MAIN PAGE ────────────────────────────────────────────────────────────────

def mis_reservas_page() -> rx.Component:
    return rx.box(
        navbar(),

        rx.box(
            rx.box(
                rx.vstack(

                    # Encabezado
                    rx.vstack(
                        rx.hstack(
                            rx.box(
                                rx.icon("ticket", size=32, color=RED_CINE),
                                width="56px", height="56px",
                                background="rgba(229,9,20,0.1)",
                                border="1px solid rgba(229,9,20,0.25)",
                                border_radius="14px", display="flex",
                                align_items="center", justify_content="center",
                                flex_shrink="0",
                            ),
                            rx.vstack(
                                rx.text(
                                    "MIS RESERVAS",
                                    font_family=FONT_HEADING,
                                    font_size=["2rem", "2.8rem"],
                                    color=WHITE, letter_spacing="2px",
                                    line_height="1",
                                ),
                                rx.hstack(
                                    rx.text("Hola,", color=GRAY_MUTED, font_size="14px"),
                                    rx.text(AppState.user_name, color=GOLD_VIP,
                                            font_size="14px", font_weight="700"),
                                    rx.text("— Historial completo de tus boletos",
                                            color=GRAY_MUTED, font_size="14px"),
                                    spacing="1", flex_wrap="wrap",
                                ),
                                align_items="start", spacing="1",
                            ),
                            spacing="4", align="center",
                        ),
                        rx.box(width="64px", height="4px", background=RED_CINE,
                               border_radius="2px"),
                        align_items="start", spacing="3", width="100%",
                    ),

                    # Stats bar
                    rx.cond(AppState.has_bookings, stats_bar(), rx.box()),

                    # Lista o estado vacío
                    rx.cond(
                        AppState.has_bookings,
                        rx.vstack(
                            # Encabezado de lista
                            rx.hstack(
                                rx.vstack(
                                    rx.text("Ordenadas de más reciente a más antigua",
                                            color=GRAY_MUTED, font_size="13px"),
                                    status_legend(),
                                    align_items="start", spacing="2",
                                ),
                                rx.spacer(),
                                rx.box(
                                    rx.text(
                                        AppState.booking_count, " reserva",
                                        rx.cond(AppState.booking_count > 1, "s", ""),
                                        color=WHITE_MUTED, font_size="13px",
                                        font_weight="600",
                                    ),
                                    padding="4px 12px",
                                    background="rgba(255,255,255,0.06)",
                                    border_radius="20px",
                                    border="1px solid rgba(255,255,255,0.1)",
                                ),
                                width="100%", align="start",
                                flex_wrap="wrap", gap="0.75rem",
                            ),

                            # Cards
                            rx.foreach(
                                AppState.booking_history,
                                lambda booking, i: booking_card(booking, i),
                            ),

                            spacing="4", width="100%", align_items="start",
                        ),
                        empty_state(),
                    ),

                    # CTA cartelera
                    rx.cond(
                        AppState.has_bookings,
                        rx.hstack(
                            rx.link(
                                rx.button(
                                    rx.hstack(
                                        rx.icon("clapperboard", size=16),
                                        rx.text("Explorar más películas"),
                                        spacing="2", align="center",
                                    ),
                                    background="transparent", color=WHITE_SOFT,
                                    border="1px solid rgba(255,255,255,0.15)",
                                    border_radius="10px", padding="12px 24px",
                                    font_size="14px", font_weight="600",
                                    cursor="pointer", transition="all 0.2s ease",
                                    _hover={"border_color": RED_CINE, "color": WHITE,
                                            "background": "rgba(229,9,20,0.06)"},
                                ),
                                href="/catalogo", text_decoration="none",
                            ),
                            justify="center", width="100%", padding_top="1rem",
                        ),
                        rx.box(),
                    ),

                    align_items="flex-start", spacing="6", width="100%",
                ),

                max_width="900px", margin="0 auto",
                padding=["6rem 1.5rem 4rem", "7rem 2rem 4rem", "8rem 3rem 4rem"],
            ),

            background=BLACK_CINEMA, min_height="100vh",
        ),

        footer(),
        toast(),
        mis_reservas_ticket_modal(),

        font_family=FONT_BODY, background=BLACK_CINEMA,
    )

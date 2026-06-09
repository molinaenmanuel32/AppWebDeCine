"""
pages/reservas.py
Sistema visual de selección de asientos con modal de pago.
"""
import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.components.navbar import navbar
from cinemax.components.footer import footer
from cinemax.components.toast import toast
from cinemax.states.app_state import AppState


ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]
SEATS_PER_ROW = 10


def seat_button(row: str, num: int) -> rx.Component:
    seat_id = f"{row}{num}"
    is_reserved = AppState.reserved_seats.contains(seat_id)
    is_selected = AppState.selected_seats.contains(seat_id)

    return rx.button(
        seat_id,
        on_click=AppState.toggle_seat(seat_id),
        background=rx.cond(
            is_reserved,
            "rgba(255,255,255,0.08)",
            rx.cond(is_selected, RED_CINE, "rgba(255,255,255,0.06)"),
        ),
        color=rx.cond(
            is_reserved,
            "rgba(255,255,255,0.2)",
            rx.cond(is_selected, WHITE, WHITE_MUTED),
        ),
        border=rx.cond(
            is_reserved,
            "1px solid rgba(255,255,255,0.06)",
            rx.cond(is_selected, f"1px solid {RED_CINE}", "1px solid rgba(255,255,255,0.12)"),
        ),
        border_radius="6px",
        padding="6px",
        font_size="10px",
        font_weight="600",
        cursor=rx.cond(is_reserved, "not-allowed", "pointer"),
        transition="all 0.15s ease",
        width="40px",
        height="36px",
        opacity=rx.cond(is_reserved, "0.4", "1"),
    )


def seat_row(row: str) -> rx.Component:
    return rx.hstack(
        rx.text(row, color=GRAY_MUTED, font_size="12px", font_weight="700", width="16px", text_align="center"),
        rx.hstack(
            *[seat_button(row, i) for i in range(1, SEATS_PER_ROW + 1)],
            spacing="1",
        ),
        rx.text(row, color=GRAY_MUTED, font_size="12px", font_weight="700", width="16px", text_align="center"),
        spacing="2",
        align="center",
    )


# ─── PAYMENT METHOD CARD ──────────────────────────────────────────────────────

def payment_method_card(icon: str, title: str, subtitle: str, method_id: str, color: str) -> rx.Component:
    is_selected = AppState.selected_payment_method == method_id
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text(icon, font_size="28px"),
                width="52px",
                height="52px",
                display="flex",
                align_items="center",
                justify_content="center",
                background=f"rgba({color}, 0.12)",
                border_radius="12px",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(title, color=WHITE, font_size="15px", font_weight="700"),
                rx.text(subtitle, color=GRAY_MUTED, font_size="12px"),
                align_items="start",
                spacing="1",
                flex="1",
            ),
            rx.cond(
                is_selected,
                rx.box(
                    rx.icon("check", size=16, color=WHITE),
                    width="28px",
                    height="28px",
                    background=RED_CINE,
                    border_radius="50%",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.box(
                    width="28px",
                    height="28px",
                    border=f"2px solid rgba(255,255,255,0.15)",
                    border_radius="50%",
                ),
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        on_click=AppState.select_payment_method(method_id),
        padding="1rem 1.2rem",
        background=rx.cond(
            is_selected,
            f"rgba(229,9,20,0.08)",
            "rgba(255,255,255,0.03)",
        ),
        border=rx.cond(
            is_selected,
            f"1px solid {RED_CINE}",
            "1px solid rgba(255,255,255,0.08)",
        ),
        border_radius="12px",
        cursor="pointer",
        transition="all 0.2s ease",
        width="100%",
        _hover={"background": "rgba(255,255,255,0.06)", "border_color": "rgba(255,255,255,0.2)"},
    )


# ─── STEP 1: SELECT METHOD ─────────────────────────────────────────────────────

def payment_step_select() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.text("Elige tu método de pago", color=WHITE, font_size="20px", font_weight="700"),
            rx.text("Selecciona cómo deseas pagar tu reserva", color=GRAY_MUTED, font_size="13px"),
            align_items="start",
            spacing="1",
        ),

        rx.vstack(
            payment_method_card("💳", "Tarjeta de Crédito/Débito", "Visa, Mastercard, AMEX", "card", "229, 9, 20"),
            payment_method_card("📱", "MobilePay", "Paga desde tu billetera digital", "wallet", "245, 197, 24"),
            payment_method_card("🏦", "CineTransfer", "Transferencia bancaria instantánea", "transfer", "0, 180, 120"),
            payment_method_card("💵", "CineCredits", "Usa tu saldo de la cuenta KankyCine", "credits", "100, 100, 255"),
            spacing="3",
            width="100%",
        ),

        rx.button(
            rx.hstack(rx.text("Continuar"), rx.icon("arrow-right", size=16), spacing="2", align="center"),
            on_click=rx.cond(
                AppState.selected_payment_method != "",
                AppState.select_payment_method(AppState.selected_payment_method),
                rx.noop(),
            ),
            background=rx.cond(
                AppState.selected_payment_method != "",
                RED_CINE,
                "rgba(255,255,255,0.08)",
            ),
            color=rx.cond(
                AppState.selected_payment_method != "",
                WHITE,
                WHITE_MUTED,
            ),
            border="none",
            border_radius="10px",
            padding="14px",
            font_size="15px",
            font_weight="700",
            cursor=rx.cond(
                AppState.selected_payment_method != "",
                "pointer",
                "not-allowed",
            ),
            width="100%",
        ),

        spacing="5",
        width="100%",
    )


# ─── INPUT HELPER ─────────────────────────────────────────────────────────────

def pay_input(label: str, placeholder: str, value, on_change, input_type: str = "text") -> rx.Component:
    return rx.vstack(
        rx.text(label, color=WHITE_MUTED, font_size="12px", font_weight="600"),
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            type=input_type,
            background=GRAY_MID,
            border=f"1px solid rgba(255,255,255,0.1)",
            border_radius="8px",
            color=WHITE,
            padding="10px 14px",
            font_size="14px",
            width="100%",
            _focus={"border_color": RED_CINE, "outline": "none", "box_shadow": f"0 0 0 2px rgba(229,9,20,0.25)"},
            _placeholder={"color": GRAY_MUTED},
        ),
        align_items="start",
        spacing="1",
        width="100%",
    )


# ─── STEP 2: FORM (per method) ────────────────────────────────────────────────

def payment_form_card() -> rx.Component:
    return rx.vstack(
        rx.text("💳 Datos de la Tarjeta", color=WHITE, font_size="16px", font_weight="700"),
        pay_input("Número de tarjeta *", "1234 5678 9012 3456", AppState.card_number, AppState.set_card_number),
        pay_input("Nombre del titular *", "Como aparece en la tarjeta", AppState.card_holder, AppState.set_card_holder),
        rx.hstack(
            pay_input("Vencimiento *", "MM/AA", AppState.card_expiry, AppState.set_card_expiry),
            pay_input("CVV *", "•••", AppState.card_cvv, AppState.set_card_cvv),
            spacing="3",
            width="100%",
        ),
        rx.box(
            rx.hstack(
                rx.icon("shield-check", size=14, color="#00c07f"),
                rx.text("Pago 100% seguro • Encriptado SSL", color="#00c07f", font_size="12px"),
                spacing="2",
                align="center",
            ),
            padding="8px 12px",
            background="rgba(0,192,127,0.08)",
            border="1px solid rgba(0,192,127,0.2)",
            border_radius="8px",
        ),
        spacing="4",
        width="100%",
    )


def payment_form_wallet() -> rx.Component:
    return rx.vstack(
        rx.text("📱 MobilePay", color=WHITE, font_size="16px", font_weight="700"),
        rx.text("Recibirás una notificación push para aprobar el pago.", color=GRAY_MUTED, font_size="13px"),
        pay_input("Número de teléfono *", "+1 (809) 000-0000", AppState.wallet_phone, AppState.set_wallet_phone, "tel"),
        rx.box(
            rx.hstack(
                rx.icon("smartphone", size=14, color=GOLD_VIP),
                rx.text("Asegúrate de tener la app MobilePay instalada", color=GOLD_VIP, font_size="12px"),
                spacing="2",
                align="center",
            ),
            padding="8px 12px",
            background="rgba(245,197,24,0.08)",
            border="1px solid rgba(245,197,24,0.2)",
            border_radius="8px",
        ),
        spacing="4",
        width="100%",
    )


def payment_form_transfer() -> rx.Component:
    return rx.vstack(
        rx.text("🏦 CineTransfer", color=WHITE, font_size="16px", font_weight="700"),
        rx.text("Transfiere desde tu banco de forma instantánea.", color=GRAY_MUTED, font_size="13px"),
        pay_input("Banco de origen *", "Ej: Banco Popular, BHD, Scotiabank", AppState.transfer_bank, AppState.set_transfer_bank),
        pay_input("Número de cuenta / RNC *", "000-000000-0", AppState.transfer_account, AppState.set_transfer_account),
        rx.box(
            rx.vstack(
                rx.text("Cuenta destino KankyCine:", color=WHITE_MUTED, font_size="12px", font_weight="700"),
                rx.text("Banco: CineBank Nacional", color=GRAY_MUTED, font_size="12px"),
                rx.text("Cuenta: 001-234567-8 (CTA. CTE)", color=GRAY_MUTED, font_size="12px"),
                rx.text("Titular: KankyCine Entertainment S.A.", color=GRAY_MUTED, font_size="12px"),
                align_items="start",
                spacing="1",
            ),
            padding="12px",
            background="rgba(0,180,120,0.08)",
            border="1px solid rgba(0,180,120,0.2)",
            border_radius="8px",
        ),
        spacing="4",
        width="100%",
    )


def payment_form_credits() -> rx.Component:
    return rx.vstack(
        rx.text("💵 CineCredits", color=WHITE, font_size="16px", font_weight="700"),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("Saldo disponible:", color=WHITE_MUTED, font_size="13px"),
                    rx.text("RD$ 2,500.00", color=GOLD_VIP, font_size="18px", font_weight="800"),
                    justify="between",
                    width="100%",
                    align="center",
                ),
                rx.box(width="100%", height="1px", background="rgba(255,255,255,0.08)"),
                rx.hstack(
                    rx.text("A descontar:", color=WHITE_MUTED, font_size="13px"),
                    rx.text("RD$ ", AppState.total_price, color=RED_CINE, font_size="16px", font_weight="700"),
                    justify="between",
                    width="100%",
                    align="center",
                ),
                spacing="3",
            ),
            padding="1rem",
            background="rgba(100,100,255,0.06)",
            border="1px solid rgba(100,100,255,0.2)",
            border_radius="10px",
        ),
        rx.text("Al confirmar, el monto se descontará automáticamente de tu saldo CineCredits.", color=GRAY_MUTED, font_size="12px"),
        spacing="4",
        width="100%",
    )


def payment_step_form() -> rx.Component:
    return rx.vstack(
        # Back button
        rx.button(
            rx.hstack(rx.icon("arrow-left", size=15), rx.text("Cambiar método"), spacing="2", align="center"),
            on_click=AppState.go_back_to_methods,
            background="transparent",
            color=GRAY_MUTED,
            border="1px solid rgba(255,255,255,0.1)",
            border_radius="8px",
            padding="8px 14px",
            font_size="13px",
            cursor="pointer",
            _hover={"color": WHITE, "border_color": "rgba(255,255,255,0.3)"},
        ),

        # Dynamic form
        rx.cond(AppState.selected_payment_method == "card", payment_form_card(), rx.box()),
        rx.cond(AppState.selected_payment_method == "wallet", payment_form_wallet(), rx.box()),
        rx.cond(AppState.selected_payment_method == "transfer", payment_form_transfer(), rx.box()),
        rx.cond(AppState.selected_payment_method == "credits", payment_form_credits(), rx.box()),

        # Error message
        rx.cond(
            AppState.payment_error != "",
            rx.box(
                rx.hstack(
                    rx.icon("triangle-alert", size=15, color="#ff6b6b"),
                    rx.text(AppState.payment_error, color="#ff6b6b", font_size="13px"),
                    spacing="2",
                    align="center",
                ),
                padding="10px 14px",
                background="rgba(255,107,107,0.1)",
                border="1px solid rgba(255,107,107,0.3)",
                border_radius="8px",
                width="100%",
            ),
            rx.box(),
        ),

        # Order summary mini
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text("Asientos", color=GRAY_MUTED, font_size="12px"),
                    rx.text(AppState.selected_seats.join(", "), color=WHITE, font_size="13px", font_weight="600"),
                    align_items="start", spacing="0",
                ),
                rx.vstack(
                    rx.text("Total", color=GRAY_MUTED, font_size="12px"),
                    rx.text("RD$ ", AppState.total_price, color=GOLD_VIP, font_size="18px", font_weight="800"),
                    align_items="end", spacing="0",
                ),
                justify="between",
                width="100%",
                align="center",
            ),
            padding="1rem",
            background="rgba(255,255,255,0.03)",
            border="1px solid rgba(255,255,255,0.08)",
            border_radius="10px",
        ),

        rx.button(
            rx.hstack(rx.icon("credit-card", size=18), rx.text("Pagar ahora"), spacing="2", align="center"),
            on_click=AppState.process_payment,
            background=RED_CINE,
            color=WHITE,
            border="none",
            border_radius="10px",
            padding="14px",
            font_size="15px",
            font_weight="700",
            cursor="pointer",
            width="100%",
            _hover={"background": RED_HOVER, "transform": "translateY(-1px)", "box_shadow": "0 6px 20px rgba(229,9,20,0.4)"},
            transition="all 0.2s ease",
        ),

        spacing="4",
        width="100%",
        align_items="start",
    )


# ─── STEP 3: PROCESSING ───────────────────────────────────────────────────────

def payment_step_processing() -> rx.Component:
    return rx.vstack(
        rx.box(height="20px"),
        rx.box(
            rx.spinner(size="3", color=RED_CINE),
            display="flex",
            justify_content="center",
        ),
        rx.vstack(
            rx.text("Procesando tu pago...", color=WHITE, font_size="20px", font_weight="700", text_align="center"),
            rx.text("Por favor no cierres esta ventana.", color=GRAY_MUTED, font_size="13px", text_align="center"),
            align_items="center",
            spacing="2",
        ),
        rx.box(height="20px"),
        rx.button(
            "Confirmar pago (simulado)",
            on_click=AppState.finalize_payment,
            background="rgba(0,192,127,0.15)",
            color="#00c07f",
            border="1px solid rgba(0,192,127,0.3)",
            border_radius="10px",
            padding="12px",
            font_size="14px",
            font_weight="600",
            cursor="pointer",
            width="100%",
        ),
        spacing="5",
        width="100%",
        align_items="center",
    )


# ─── PAYMENT MODAL ────────────────────────────────────────────────────────────

def payment_modal() -> rx.Component:
    return rx.cond(
        AppState.show_payment_modal,
        rx.box(
            # Overlay
            rx.box(
                on_click=AppState.close_payment_modal,
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background="rgba(0,0,0,0.75)",
                z_index="1000",
                backdrop_filter="blur(4px)",
            ),
            # Modal panel
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.text("MÉTODO DE PAGO", color=GRAY_MUTED, font_size="11px", font_weight="700", letter_spacing="2"),
                            rx.text("KankyCine Checkout", color=WHITE, font_size="18px", font_weight="800"),
                            align_items="start",
                            spacing="0",
                        ),
                        rx.button(
                            rx.icon("x", size=18),
                            on_click=AppState.close_payment_modal,
                            background="rgba(255,255,255,0.08)",
                            color=WHITE,
                            border="none",
                            border_radius="8px",
                            padding="8px",
                            cursor="pointer",
                            _hover={"background": "rgba(255,255,255,0.15)"},
                        ),
                        justify="between",
                        width="100%",
                        align="center",
                    ),

                    rx.box(width="100%", height="1px", background="rgba(255,255,255,0.08)"),

                    # Dynamic content
                    rx.cond(AppState.payment_step == "select", payment_step_select(), rx.box()),
                    rx.cond(AppState.payment_step == "form", payment_step_form(), rx.box()),
                    rx.cond(AppState.payment_step == "processing", payment_step_processing(), rx.box()),

                    spacing="4",
                    width="100%",
                    padding="1.5rem",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                background=GRAY_DARK,
                border="1px solid rgba(255,255,255,0.1)",
                border_radius="20px",
                width=["92vw", "480px"],
                max_height="90vh",
                overflow_y="auto",
                z_index="1001",
                box_shadow="0 40px 80px rgba(0,0,0,0.8)",
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            z_index="999",
        ),
        rx.box(),
    )


# ─── QR CODE SVG ──────────────────────────────────────────────────────────────

def qr_svg() -> rx.Component:
    """QR code visual decorativo."""
    return rx.html("""
    <svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
      <rect width="120" height="120" fill="#1a1a1a" rx="8"/>
      <!-- Top-left finder pattern -->
      <rect x="10" y="10" width="30" height="30" fill="none" stroke="#e50914" stroke-width="3" rx="2"/>
      <rect x="17" y="17" width="16" height="16" fill="#e50914" rx="1"/>
      <!-- Top-right finder pattern -->
      <rect x="80" y="10" width="30" height="30" fill="none" stroke="#e50914" stroke-width="3" rx="2"/>
      <rect x="87" y="17" width="16" height="16" fill="#e50914" rx="1"/>
      <!-- Bottom-left finder pattern -->
      <rect x="10" y="80" width="30" height="30" fill="none" stroke="#e50914" stroke-width="3" rx="2"/>
      <rect x="17" y="87" width="16" height="16" fill="#e50914" rx="1"/>
      <!-- Data modules (random pattern) -->
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
      <rect x="50" y="90" width="6" height="6" fill="white" rx="1"/>
      <rect x="60" y="90" width="6" height="6" fill="white" rx="1"/>
      <rect x="80" y="90" width="6" height="6" fill="white" rx="1"/>
      <rect x="90" y="80" width="6" height="6" fill="white" rx="1"/>
      <rect x="100" y="80" width="6" height="6" fill="white" rx="1"/>
      <rect x="100" y="90" width="6" height="6" fill="white" rx="1"/>
      <rect x="90" y="100" width="6" height="6" fill="white" rx="1"/>
    </svg>
    """)


# ─── TICKET MODAL ─────────────────────────────────────────────────────────────

def ticket_modal() -> rx.Component:
    return rx.cond(
        AppState.show_ticket,
        rx.box(
            # Overlay
            rx.box(
                on_click=AppState.close_ticket,
                position="fixed",
                top="0", left="0", right="0", bottom="0",
                background="rgba(0,0,0,0.85)",
                z_index="2000",
                backdrop_filter="blur(6px)",
            ),
            # Ticket panel
            rx.box(
                rx.vstack(
                    # Header del ticket
                    rx.vstack(
                        rx.hstack(
                            rx.text("🎬", font_size="28px"),
                            rx.vstack(
                                rx.text("KANKYCINE", color=RED_CINE, font_size="22px", font_weight="900", letter_spacing="4"),
                                rx.text("ENTERTAINMENT", color=GRAY_MUTED, font_size="9px", letter_spacing="6"),
                                spacing="0",
                                align_items="start",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        rx.box(width="100%", height="2px",
                               background=f"linear-gradient(90deg, transparent, {RED_CINE}, transparent)"),
                        rx.text("✓ RESERVA CONFIRMADA", color="#00c07f", font_size="13px",
                                font_weight="700", letter_spacing="2"),
                        align_items="center",
                        spacing="3",
                        padding="1.5rem 1.5rem 1rem",
                        background=f"linear-gradient(180deg, rgba(229,9,20,0.08) 0%, transparent 100%)",
                        width="100%",
                        border_radius="20px 20px 0 0",
                    ),

                    # Contenido del ticket
                    rx.vstack(
                        # Película
                        rx.vstack(
                            rx.text("PELÍCULA", color=GRAY_MUTED, font_size="10px",
                                    font_weight="700", letter_spacing="3"),
                            rx.text(AppState.ticket_movie, color=WHITE, font_size="18px",
                                    font_weight="800", text_align="center"),
                            align_items="center", spacing="1",
                        ),

                        # Separador punteado
                        rx.box(
                            width="100%", height="1px",
                            background="repeating-linear-gradient(90deg, rgba(255,255,255,0.2) 0, rgba(255,255,255,0.2) 8px, transparent 8px, transparent 16px)",
                            margin="0.5rem 0",
                        ),

                        # Info en grid
                        rx.grid(
                            # Sala
                            rx.vstack(
                                rx.text("SALA", color=GRAY_MUTED, font_size="10px",
                                        font_weight="700", letter_spacing="2"),
                                rx.text(AppState.ticket_hall, color=WHITE,
                                        font_size="16px", font_weight="700"),
                                align_items="center", spacing="1",
                            ),
                            # Horario
                            rx.vstack(
                                rx.text("HORARIO", color=GRAY_MUTED, font_size="10px",
                                        font_weight="700", letter_spacing="2"),
                                rx.text(AppState.ticket_showtime, color=WHITE,
                                        font_size="16px", font_weight="700"),
                                align_items="center", spacing="1",
                            ),
                            # Fecha
                            rx.vstack(
                                rx.text("FECHA", color=GRAY_MUTED, font_size="10px",
                                        font_weight="700", letter_spacing="2"),
                                rx.text(AppState.ticket_date, color=WHITE,
                                        font_size="13px", font_weight="600"),
                                align_items="center", spacing="1",
                            ),
                            columns="3",
                            gap="1rem",
                            width="100%",
                        ),

                        # Separador punteado
                        rx.box(
                            width="100%", height="1px",
                            background="repeating-linear-gradient(90deg, rgba(255,255,255,0.2) 0, rgba(255,255,255,0.2) 8px, transparent 8px, transparent 16px)",
                            margin="0.25rem 0",
                        ),

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

                        # Separador punteado
                        rx.box(
                            width="100%", height="1px",
                            background="repeating-linear-gradient(90deg, rgba(255,255,255,0.2) 0, rgba(255,255,255,0.2) 8px, transparent 8px, transparent 16px)",
                            margin="0.25rem 0",
                        ),

                        rx.vstack(
                            rx.text("ASIENTOS", color=GRAY_MUTED, font_size="10px",
                                    font_weight="700", letter_spacing="3"),
                            rx.box(
                                rx.foreach(
                                    AppState.ticket_seats,
                                    lambda s: rx.box(
                                        s,
                                        background=RED_CINE,
                                        color=WHITE,
                                        font_size="12px",
                                        font_weight="700",
                                        padding="4px 10px",
                                        border_radius="6px",
                                    )
                                ),
                                display="flex",
                                flex_wrap="wrap",
                                gap="0.5rem",
                                justify_content="center",
                            ),
                            align_items="center", spacing="2",
                        ),

                        # Separador punteado
                        rx.box(
                            width="100%", height="1px",
                            background="repeating-linear-gradient(90deg, rgba(255,255,255,0.2) 0, rgba(255,255,255,0.2) 8px, transparent 8px, transparent 16px)",
                            margin="0.25rem 0",
                        ),

                        # Total + QR
                        rx.hstack(
                            # Total
                            rx.vstack(
                                rx.text("TOTAL PAGADO", color=GRAY_MUTED, font_size="10px",
                                        font_weight="700", letter_spacing="2"),
                                rx.text("RD$ ", AppState.ticket_total, color=GOLD_VIP,
                                        font_size="24px", font_weight="900"),
                                align_items="start",
                                spacing="1",
                            ),
                            rx.spacer(),
                            # QR
                            rx.vstack(
                                qr_svg(),
                                rx.text(AppState.ticket_code, color=GRAY_MUTED,
                                        font_size="9px", font_weight="600",
                                        letter_spacing="1", text_align="center"),
                                align_items="center",
                                spacing="1",
                            ),
                            width="100%",
                            align="center",
                        ),

                        padding="1rem 1.5rem 1.5rem",
                        spacing="4",
                        width="100%",
                    ),

                    # Footer del ticket
                    rx.vstack(
                        rx.box(
                            width="100%", height="1px",
                            background="rgba(255,255,255,0.08)",
                        ),
                        rx.text(
                            "Presenta este ticket en la entrada del cine. Válido solo para la función indicada.",
                            color=GRAY_MUTED, font_size="11px", text_align="center",
                            padding="0 1rem",
                        ),
                        rx.button(
                            rx.hstack(rx.icon("check", size=16), rx.text("Cerrar"), spacing="2", align="center"),
                            on_click=AppState.close_ticket,
                            background=RED_CINE,
                            color=WHITE,
                            border="none",
                            border_radius="10px",
                            padding="12px 32px",
                            font_size="14px",
                            font_weight="700",
                            cursor="pointer",
                            width="100%",
                            margin="0 1rem",
                            _hover={"background": RED_HOVER},
                        ),
                        spacing="3",
                        padding="1rem 1rem 1.5rem",
                        align_items="center",
                        width="100%",
                        background="rgba(255,255,255,0.02)",
                        border_radius="0 0 20px 20px",
                    ),

                    spacing="0",
                    width="100%",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                background=GRAY_DARK,
                border="1px solid rgba(229,9,20,0.3)",
                border_radius="20px",
                width=["92vw", "440px"],
                max_height="92vh",
                overflow_y="auto",
                z_index="2001",
                box_shadow="0 40px 80px rgba(0,0,0,0.9), 0 0 0 1px rgba(229,9,20,0.1)",
            ),
            position="fixed",
            top="0", left="0", right="0", bottom="0",
            z_index="1999",
        ),
        rx.box(),
    )



# ─── AUTH REQUIRED MODAL ──────────────────────────────────────────────────────

def auth_required_modal() -> rx.Component:
    return rx.cond(
        AppState.show_auth_required_modal,
        rx.box(
            # Overlay
            rx.box(
                on_click=AppState.close_auth_required_modal,
                position="fixed",
                top="0", left="0", right="0", bottom="0",
                background="rgba(0,0,0,0.80)",
                z_index="1200",
                backdrop_filter="blur(6px)",
            ),
            # Modal panel
            rx.box(
                rx.vstack(
                    # Ícono
                    rx.box(
                        rx.text("🔒", font_size="48px"),
                        display="flex",
                        justify_content="center",
                        padding_bottom="0.5rem",
                    ),
                    # Título
                    rx.text(
                        "Inicia sesión para continuar",
                        color=WHITE,
                        font_size="22px",
                        font_weight="800",
                        text_align="center",
                        font_family=FONT_HEADING,
                    ),
                    # Descripción
                    rx.text(
                        "Necesitas una cuenta para reservar tus boletos. ¡Es rápido y gratis!",
                        color=GRAY_MUTED,
                        font_size="14px",
                        text_align="center",
                        line_height="1.6",
                        max_width="320px",
                    ),
                    rx.box(height="4px"),
                    # Botones
                    rx.vstack(
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("log-in", size=18),
                                    rx.text("Iniciar sesión"),
                                    spacing="2",
                                    align="center",
                                ),
                                background=RED_CINE,
                                color=WHITE,
                                border="none",
                                border_radius="10px",
                                padding="14px",
                                font_size="15px",
                                font_weight="700",
                                cursor="pointer",
                                width="100%",
                                transition="all 0.2s ease",
                                _hover={
                                    "background": RED_HOVER,
                                    "transform": "translateY(-1px)",
                                    "box_shadow": "0 6px 20px rgba(229,9,20,0.4)",
                                },
                            ),
                            href="/login",
                            text_decoration="none",
                            width="100%",
                        ),
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("user-plus", size=18),
                                    rx.text("Registrarte"),
                                    spacing="2",
                                    align="center",
                                ),
                                background="transparent",
                                color=WHITE,
                                border=f"2px solid {RED_CINE}",
                                border_radius="10px",
                                padding="14px",
                                font_size="15px",
                                font_weight="700",
                                cursor="pointer",
                                width="100%",
                                transition="all 0.2s ease",
                                _hover={
                                    "background": "rgba(229,9,20,0.1)",
                                    "transform": "translateY(-1px)",
                                },
                            ),
                            href="/registro",
                            text_decoration="none",
                            width="100%",
                        ),
                        rx.button(
                            "Cancelar",
                            on_click=AppState.close_auth_required_modal,
                            background="transparent",
                            color=GRAY_MUTED,
                            border="1px solid rgba(255,255,255,0.1)",
                            border_radius="8px",
                            padding="10px",
                            font_size="13px",
                            cursor="pointer",
                            width="100%",
                            _hover={"color": WHITE, "border_color": "rgba(255,255,255,0.3)"},
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    align_items="center",
                    spacing="4",
                    padding="2rem",
                    width="100%",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                background=GRAY_DARK,
                border="1px solid rgba(229,9,20,0.3)",
                border_radius="20px",
                width=["90vw", "400px"],
                z_index="1201",
                box_shadow="0 40px 80px rgba(0,0,0,0.9), 0 0 0 1px rgba(229,9,20,0.1)",
            ),
            position="fixed",
            top="0", left="0", right="0", bottom="0",
            z_index="1199",
        ),
        rx.box(),
    )

# ─── MAIN PAGE ────────────────────────────────────────────────────────────────

def reservas_page() -> rx.Component:
    return rx.box(
        navbar(),

        rx.box(
            rx.box(
                rx.vstack(
                    rx.vstack(
                        rx.text("SELECCIÓN DE ASIENTOS", font_family=FONT_HEADING, font_size=["2.5rem", "3.5rem"], color=WHITE, letter_spacing="1"),
                        rx.box(width="64px", height="4px", background=RED_CINE, border_radius="2px"),
                        align_items="start",
                        spacing="2",
                        margin_bottom="0.5rem",
                    ),

                    # Info de la sala actual
                    rx.cond(
                        AppState.movie_loaded,
                        rx.hstack(
                            rx.icon("ticket", size=16, color=RED_CINE),
                            rx.text(
                                AppState.current_movie["nombre"],
                                color=WHITE_MUTED,
                                font_size="15px",
                                font_weight="600",
                            ),
                            rx.text("•", color=GRAY_MUTED),
                            rx.text(
                                "Sala ",
                                AppState.current_movie["id"],
                                color=GRAY_MUTED,
                                font_size="14px",
                            ),
                            spacing="2",
                            align="center",
                            padding="8px 16px",
                            background="rgba(229,9,20,0.06)",
                            border="1px solid rgba(229,9,20,0.2)",
                            border_radius="8px",
                            display="inline-flex",
                        ),
                        rx.box(),
                    ),

                    rx.flex(
                        # Seat Map
                        rx.vstack(
                            rx.box(
                                rx.text("PANTALLA", color=WHITE_MUTED, font_size="11px", font_weight="700", letter_spacing="1", text_align="center"),
                                background="linear-gradient(180deg, rgba(229,9,20,0.2) 0%, transparent 100%)",
                                border_top=f"3px solid {RED_CINE}",
                                border_radius="0 0 50% 50%",
                                padding="10px 0 20px",
                                width="80%",
                                margin_bottom="2rem",
                            ),
                            rx.vstack(
                                *[seat_row(row) for row in ROWS],
                                spacing="2",
                            ),
                            rx.hstack(
                                rx.hstack(
                                    rx.box(width="20px", height="20px", background=RED_CINE, border_radius="4px"),
                                    rx.text("Seleccionado", color=WHITE_MUTED, font_size="12px"),
                                    spacing="2", align="center",
                                ),
                                rx.hstack(
                                    rx.box(width="20px", height="20px", background="rgba(255,255,255,0.06)", border="1px solid rgba(255,255,255,0.12)", border_radius="4px"),
                                    rx.text("Disponible", color=WHITE_MUTED, font_size="12px"),
                                    spacing="2", align="center",
                                ),
                                rx.hstack(
                                    rx.box(width="20px", height="20px", background="rgba(255,255,255,0.08)", border_radius="4px", opacity="0.4"),
                                    rx.text("Ocupado", color=WHITE_MUTED, font_size="12px"),
                                    spacing="2", align="center",
                                ),
                                spacing="6",
                                flex_wrap="wrap",
                                margin_top="2rem",
                            ),
                            align_items="center",
                            flex="1",
                            padding="2rem",
                            background=GRAY_DARK,
                            border_radius="16px",
                            border="1px solid rgba(255,255,255,0.06)",
                        ),

                        # Summary Panel
                        rx.vstack(
                            rx.text("RESUMEN DE COMPRA", color=WHITE_MUTED, font_size="11px", font_weight="700", letter_spacing="1"),

                            rx.vstack(
                                rx.text("Película", color=GRAY_MUTED, font_size="12px"),
                                rx.text(
                                    rx.cond(
                                        AppState.movie_loaded,
                                        AppState.current_movie["nombre"],
                                        "Sin seleccionar",
                                    ),
                                    color=WHITE, font_size="15px", font_weight="600",
                                ),
                                align_items="start", spacing="1",
                                padding="1rem",
                                background="rgba(255,255,255,0.03)",
                                border_radius="10px",
                                width="100%",
                                border="1px solid rgba(255,255,255,0.06)",
                            ),

                            rx.vstack(
                                rx.text("Sala", color=GRAY_MUTED, font_size="12px"),
                                rx.text(
                                    rx.cond(
                                        AppState.movie_loaded,
                                        rx.fragment("Sala ", AppState.current_movie["id"]),
                                        "—",
                                    ),
                                    color=WHITE, font_size="15px", font_weight="600",
                                ),
                                align_items="start", spacing="1",
                                padding="1rem",
                                background="rgba(255,255,255,0.03)",
                                border_radius="10px",
                                width="100%",
                                border="1px solid rgba(255,255,255,0.06)",
                            ),

                            rx.vstack(
                                rx.text("Función", color=GRAY_MUTED, font_size="12px"),
                                rx.text(
                                    rx.cond(
                                        AppState.selected_showtime != "",
                                        AppState.selected_showtime,
                                        "No seleccionada",
                                    ),
                                    color=WHITE, font_size="15px", font_weight="600",
                                ),
                                align_items="start", spacing="1",
                                padding="1rem",
                                background="rgba(255,255,255,0.03)",
                                border_radius="10px",
                                width="100%",
                                border="1px solid rgba(255,255,255,0.06)",
                            ),

                            rx.vstack(
                                rx.text("Asientos seleccionados", color=GRAY_MUTED, font_size="12px"),
                                rx.text(
                                    rx.cond(
                                        AppState.seat_count > 0,
                                        AppState.selected_seats.join(", "),
                                        "Ninguno",
                                    ),
                                    color=WHITE, font_size="14px", font_weight="600",
                                ),
                                align_items="start", spacing="1",
                                padding="1rem",
                                background="rgba(255,255,255,0.03)",
                                border_radius="10px",
                                width="100%",
                                border="1px solid rgba(255,255,255,0.06)",
                            ),

                            rx.divider(border_color="rgba(255,255,255,0.08)"),

                            rx.hstack(
                                rx.text("TOTAL", color=WHITE_MUTED, font_size="14px", font_weight="700"),
                                rx.text(
                                    "RD$ ", AppState.total_price,
                                    color=GOLD_VIP, font_size="1.4rem", font_weight="800",
                                ),
                                justify="between",
                                width="100%",
                                align="center",
                            ),

                            rx.button(
                                rx.hstack(
                                    rx.icon("check", size=18),
                                    rx.text("Confirmar Reserva"),
                                    spacing="2", align="center",
                                ),
                                on_click=AppState.confirm_reservation,
                                background=rx.cond(AppState.seat_count > 0, RED_CINE, "rgba(255,255,255,0.08)"),
                                color=rx.cond(AppState.seat_count > 0, WHITE, WHITE_MUTED),
                                border="none",
                                border_radius="10px",
                                padding="14px",
                                font_size="15px",
                                font_weight="700",
                                cursor=rx.cond(AppState.seat_count > 0, "pointer", "not-allowed"),
                                transition="all 0.2s ease",
                                width="100%",
                            ),

                            rx.button(
                                "Limpiar selección",
                                on_click=AppState.clear_seats,
                                background="transparent",
                                color=GRAY_MUTED,
                                border="1px solid rgba(255,255,255,0.1)",
                                border_radius="8px",
                                padding="10px",
                                font_size="13px",
                                cursor="pointer",
                                width="100%",
                                _hover={"color": WHITE, "border_color": "rgba(255,255,255,0.3)"},
                            ),

                            padding="1.5rem",
                            background=GRAY_DARK,
                            border_radius="16px",
                            border="1px solid rgba(255,255,255,0.06)",
                            min_width="280px",
                            max_width="320px",
                            align_items="start",
                            spacing="4",
                            align_self="start",
                            position="sticky",
                            top="80px",
                        ),

                        gap="2rem",
                        flex_wrap=["wrap", "wrap", "nowrap"],
                        align_items="start",
                        width="100%",
                    ),

                    align_items="flex-start",
                    spacing="5",
                    width="100%",
                ),

                max_width="1200px",
                margin="0 auto",
                padding=["6rem 1.5rem 3rem", "7rem 2rem 3rem", "8rem 4rem 3rem"],
            ),

            background=BLACK_CINEMA,
            min_height="100vh",
        ),

        footer(),
        toast(),
        payment_modal(),
        ticket_modal(),
        auth_required_modal(),
        font_family=FONT_BODY,
        background=BLACK_CINEMA,
    )
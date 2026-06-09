"""
components/navbar.py
Navbar premium estilo Netflix — con enlace "Mis Reservas" para usuarios autenticados.
"""

import reflex as rx
from cinemax.pages.styles.theme import *
from cinemax.states.app_state import AppState


def nav_link(label: str, href: str) -> rx.Component:
    return rx.link(
        label,
        href=href,
        color=WHITE_SOFT,
        font_size="14px",
        font_weight="500",
        text_decoration="none",
        padding="6px 0",
        transition="color 0.2s ease",
        _hover={"color": WHITE},
    )


def branch_selector() -> rx.Component:
    """Selector de sucursal — visible en desktop y mobile."""
    return rx.menu.root(
        rx.menu.trigger(
            rx.hstack(
                rx.icon("map-pin", size=14, color=GOLD_VIP),
                rx.text(
                    AppState.selected_branch,
                    color=GOLD_VIP,
                    font_size="13px",
                    font_weight="600",
                    max_width="120px",
                    overflow="hidden",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                ),
                rx.icon("chevron-down", size=12, color=GOLD_VIP),
                spacing="1",
                align="center",
                cursor="pointer",
                padding="6px 10px",
                border_radius="8px",
                border=f"1px solid rgba(212,175,55,0.3)",
                background="rgba(212,175,55,0.06)",
                transition="all 0.2s ease",
                _hover={"background": "rgba(212,175,55,0.12)", "border_color": GOLD_VIP},
            )
        ),
        rx.menu.content(
            rx.text(
                "SELECCIONAR SUCURSAL",
                color=GRAY_MUTED,
                font_size="10px",
                font_weight="700",
                letter_spacing="2px",
                padding="8px 12px 4px",
            ),
            rx.menu.item(
                rx.hstack(
                    rx.icon("map-pin", size=13),
                    rx.text("Downtown Center"),
                    rx.cond(AppState.selected_branch == "Downtown Center",
                            rx.icon("check", size=13, color=GOLD_VIP),
                            rx.box()),
                    spacing="2", align="center", justify="between", width="100%",
                ),
                on_click=AppState.set_branch("Downtown Center"),
                color=rx.cond(AppState.selected_branch == "Downtown Center", GOLD_VIP, WHITE_SOFT),
                font_weight=rx.cond(AppState.selected_branch == "Downtown Center", "600", "400"),
            ),
            rx.menu.item(
                rx.hstack(
                    rx.icon("map-pin", size=13),
                    rx.text("Agora Mall"),
                    rx.cond(AppState.selected_branch == "Agora Mall",
                            rx.icon("check", size=13, color=GOLD_VIP),
                            rx.box()),
                    spacing="2", align="center", justify="between", width="100%",
                ),
                on_click=AppState.set_branch("Agora Mall"),
                color=rx.cond(AppState.selected_branch == "Agora Mall", GOLD_VIP, WHITE_SOFT),
                font_weight=rx.cond(AppState.selected_branch == "Agora Mall", "600", "400"),
            ),
            rx.menu.item(
                rx.hstack(
                    rx.icon("map-pin", size=13),
                    rx.text("Galeria 360"),
                    rx.cond(AppState.selected_branch == "Galeria 360",
                            rx.icon("check", size=13, color=GOLD_VIP),
                            rx.box()),
                    spacing="2", align="center", justify="between", width="100%",
                ),
                on_click=AppState.set_branch("Galeria 360"),
                color=rx.cond(AppState.selected_branch == "Galeria 360", GOLD_VIP, WHITE_SOFT),
                font_weight=rx.cond(AppState.selected_branch == "Galeria 360", "600", "400"),
            ),
            rx.menu.item(
                rx.hstack(
                    rx.icon("map-pin", size=13),
                    rx.text("Bluemall"),
                    rx.cond(AppState.selected_branch == "Bluemall",
                            rx.icon("check", size=13, color=GOLD_VIP),
                            rx.box()),
                    spacing="2", align="center", justify="between", width="100%",
                ),
                on_click=AppState.set_branch("Bluemall"),
                color=rx.cond(AppState.selected_branch == "Bluemall", GOLD_VIP, WHITE_SOFT),
                font_weight=rx.cond(AppState.selected_branch == "Bluemall", "600", "400"),
            ),
            background="rgba(20,20,20,0.98)",
            border="1px solid rgba(255,255,255,0.1)",
            border_radius="10px",
            min_width="200px",
            padding="4px",
        ),
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Logo
            rx.link(
                rx.hstack(
                    rx.text("K", color=RED_CINE, font_size="1.6rem", font_family=FONT_HEADING, display="inline"),
                    rx.text("ANKYCINE", color=WHITE, font_size="1.6rem", font_family=FONT_HEADING, display="inline"),
                    spacing="0",
                ),
                href="/",
                text_decoration="none",
            ),

            # Desktop Nav
            rx.hstack(
                nav_link("Inicio", "/"),
                nav_link("Cartelera", "/catalogo"),
                nav_link("VIP", "/#vip"),
                nav_link("Promociones", "/#promo"),
                # Selector de sucursal
                branch_selector(),
                # "Mis Reservas" solo visible cuando está autenticado
                rx.cond(
                    AppState.is_logged_in,
                    rx.link(
                        rx.hstack(
                            rx.icon("ticket", size=14),
                            rx.text("Mis Reservas"),
                            spacing="1",
                            align="center",
                        ),
                        href="/mis-reservas",
                        color=GOLD_VIP,
                        font_size="14px",
                        font_weight="600",
                        text_decoration="none",
                        padding="6px 0",
                        transition="color 0.2s ease",
                        _hover={"color": WHITE},
                    ),
                    rx.box(),  # nada si no está autenticado
                ),
                # Admin link — solo para administradores
                rx.cond(
                    AppState.is_admin,
                    rx.link(
                        rx.hstack(
                            rx.icon("shield-check", size=14),
                            rx.text("Admin"),
                            spacing="1",
                            align="center",
                        ),
                        href="/admin",
                        color=RED_CINE,
                        font_size="14px",
                        font_weight="700",
                        text_decoration="none",
                        padding="6px 0",
                        transition="color 0.2s ease",
                        _hover={"color": RED_HOVER},
                    ),
                    rx.box(),
                ),
                spacing="6",
                display=["none", "none", "flex"],
                align="center",
            ),

            # Auth
            rx.hstack(
                rx.cond(
                    AppState.is_logged_in,
                    rx.hstack(
                        rx.text(
                            "👤 ", AppState.user_name,
                            color=WHITE_SOFT, font_size="14px",
                        ),
                        rx.button(
                            "Salir",
                            on_click=AppState.handle_logout,
                            background="transparent",
                            color=WHITE_MUTED,
                            border="1px solid rgba(255,255,255,0.2)",
                            border_radius="6px",
                            padding="6px 14px",
                            font_size="13px",
                            cursor="pointer",
                            _hover={"color": WHITE, "border_color": "rgba(255,255,255,0.5)"},
                        ),
                        spacing="4",
                        display=["none", "none", "flex"],
                    ),
                    rx.hstack(
                        rx.link(
                            "Iniciar sesión",
                            href="/login",
                            color=WHITE_SOFT,
                            font_size="14px",
                            text_decoration="none",
                            _hover={"color": WHITE},
                            display=["none", "none", "block"],
                        ),
                        rx.link(
                            rx.button(
                                "Registrarse",
                                background=RED_CINE,
                                color=WHITE,
                                border="none",
                                border_radius="8px",
                                padding="8px 20px",
                                font_size="14px",
                                font_weight="600",
                                cursor="pointer",
                                transition="all 0.2s ease",
                                _hover={"background": RED_HOVER, "transform": "translateY(-1px)"},
                            ),
                            href="/registro",
                            text_decoration="none",
                            display=["none", "none", "block"],
                        ),
                        spacing="4",
                        align_items="center",
                    ),
                ),

                # Hamburger
                rx.button(
                    rx.icon("menu", size=22),
                    on_click=AppState.toggle_mobile_menu,
                    background="transparent",
                    border="none",
                    color=WHITE,
                    cursor="pointer",
                    display=["flex", "flex", "none"],
                    padding="4px",
                ),
                align_items="center",
                spacing="4",
            ),

            align="center",
            justify="between",
            width="100%",
        ),

        # Mobile Menu
        rx.cond(
            AppState.mobile_menu_open,
            rx.box(
                rx.vstack(
                    rx.link("Inicio", href="/", color=WHITE_SOFT, text_decoration="none", font_size="16px", padding="8px 0", width="100%"),
                    rx.link("Cartelera", href="/catalogo", color=WHITE_SOFT, text_decoration="none", font_size="16px", padding="8px 0", width="100%"),
                    rx.link("VIP", href="/#vip", color=WHITE_SOFT, text_decoration="none", font_size="16px", padding="8px 0", width="100%"),
                    # Selector de sucursal móvil
                    rx.vstack(
                        rx.text("SUCURSAL", color=GRAY_MUTED, font_size="10px",
                                font_weight="700", letter_spacing="2px", padding_top="8px"),
                        branch_selector(),
                        align_items="start", spacing="1", width="100%",
                    ),
                    # Mis Reservas en móvil — solo autenticados
                    rx.cond(
                        AppState.is_logged_in,
                        rx.link(
                            rx.hstack(
                                rx.icon("ticket", size=16, color=GOLD_VIP),
                                rx.text("Mis Reservas", color=GOLD_VIP, font_weight="600"),
                                spacing="2", align="center",
                            ),
                            href="/mis-reservas",
                            text_decoration="none",
                            font_size="16px",
                            padding="8px 0",
                            width="100%",
                        ),
                        rx.box(),
                    ),
                    rx.cond(
                        AppState.is_admin,
                        rx.link(
                            rx.hstack(
                                rx.icon("shield-check", size=16, color=RED_CINE),
                                rx.text("Admin", color=RED_CINE, font_weight="700"),
                                spacing="2", align="center",
                            ),
                            href="/admin",
                            text_decoration="none",
                            font_size="16px",
                            padding="8px 0",
                            width="100%",
                        ),
                        rx.box(),
                    ),
                    rx.divider(border_color="rgba(255,255,255,0.1)"),
                    # Auth links móvil
                    rx.cond(
                        AppState.is_logged_in,
                        rx.vstack(
                            rx.text(
                                "👤 ", AppState.user_name,
                                color=WHITE_SOFT, font_size="15px", padding="8px 0",
                            ),
                            rx.button(
                                "Cerrar sesión",
                                on_click=AppState.handle_logout,
                                background="transparent",
                                color=WHITE_MUTED,
                                border="1px solid rgba(255,255,255,0.2)",
                                border_radius="8px",
                                padding="10px 0",
                                font_size="15px",
                                cursor="pointer",
                                width="100%",
                                _hover={"color": WHITE},
                            ),
                            align_items="start",
                            spacing="1",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.link("Iniciar sesión", href="/login", color=WHITE_SOFT, text_decoration="none", font_size="16px", padding="8px 0", width="100%"),
                            rx.link(
                                rx.box("Registrarse", background=RED_CINE, color=WHITE, border_radius="8px", padding="10px 0", text_align="center", width="100%"),
                                href="/registro",
                                text_decoration="none",
                                width="100%",
                            ),
                            align_items="start",
                            spacing="2",
                            width="100%",
                        ),
                    ),
                    spacing="0",
                    align_items="start",
                    width="100%",
                    padding="1rem 2rem",
                ),
                background="rgba(10,10,10,0.98)",
                backdrop_filter="blur(10px)",
                position="absolute",
                top="64px",
                left="0",
                right="0",
                z_index="999",
                border_top="1px solid rgba(255,255,255,0.08)",
            ),
        ),

        position="fixed",
        top="0",
        left="0",
        right="0",
        z_index="1000",
        height="64px",
        padding="0 2.5rem",
        display="flex",
        align_items="center",
        background="rgba(10,10,10,0.92)",
        backdrop_filter="blur(16px)",
        border_bottom="1px solid rgba(255,255,255,0.06)",
        transition="all 0.3s ease",
    )
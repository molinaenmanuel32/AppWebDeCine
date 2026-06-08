# cinemax/pages/admin/dashboard.py
"""
Dashboard de Administración.
Protegido: redirige si el usuario no es admin.
"""

import reflex as rx
from ...states.movie_state import MovieState
from ...states.app_state import AppState
from ...components.navbar import navbar


def _stat_card(label: str, value: rx.Component, icon: str, color: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(icon, color=color, size=32),
                rx.spacer(),
                rx.text(
                    label,
                    color="#888",
                    font_size="0.85rem",
                    font_weight="600",
                    text_transform="uppercase",
                    letter_spacing="0.05em",
                ),
            ),
            rx.text(value, font_size="2.5rem", font_weight="800", color="white"),
            align="start",
            spacing="2",
        ),
        bg="#111",
        border="1px solid #222",
        border_radius="12px",
        p="6",
        _hover={"border_color": color, "transform": "translateY(-2px)"},
        transition="all 0.2s",
        cursor="default",
    )


def _movie_row(movie: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.hstack(
                rx.image(
                    src=movie["poster_url"] or "https://via.placeholder.com/40x60?text=N/A",
                    width="40px",
                    height="60px",
                    object_fit="cover",
                    border_radius="4px",
                ),
                rx.text(movie["title"], color="white", font_weight="600"),
                spacing="3",
                align="center",
            )
        ),
        rx.table.cell(rx.text(movie["genre"] or "—", color="#888")),
        rx.table.cell(
            rx.badge(
                rx.cond(movie["active"], "Activa", "Inactiva"),
                color_scheme=rx.cond(movie["active"], "green", "red"),
                variant="soft",
            )
        ),
    )


def admin_guard(content: rx.Component) -> rx.Component:
    """Wrapper que redirige si no es admin."""
    return rx.cond(
        AppState.user_role == "admin",
        content,
        rx.box(
            rx.vstack(
                rx.icon("shield-x", color="#E50914", size=64),
                rx.heading("Acceso Denegado", color="white", size="6"),
                rx.text(
                    "Solo los administradores pueden ver esta página.",
                    color="#888",
                ),
                rx.link(
                    rx.button("Ir al inicio", bg="#E50914", color="white"),
                    href="/",
                ),
                align="center",
                spacing="4",
            ),
            min_height="80vh",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
    )


@rx.page(
    route="/admin",
    title="CineMax Admin",
    on_load=[
        MovieState.admin_load_dashboard,
        MovieState.admin_load_movies,
    ],
)
def admin_dashboard_page() -> rx.Component:
    return admin_guard(
        rx.box(
            navbar(),
            rx.box(
                # Header
                rx.hstack(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("layout-dashboard", color="#E50914", size=28),
                            rx.heading("Dashboard", color="white", size="7"),
                            spacing="3",
                            align="center",
                        ),
                        rx.text(
                            "Panel de administración de CineMax",
                            color="#888",
                            font_size="0.95rem",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.spacer(),
                    rx.link(
                        rx.button(
                            rx.icon("film", size=16),
                            "Gestionar Películas",
                            bg="#E50914",
                            color="white",
                            _hover={"bg": "#b0060f"},
                        ),
                        href="/admin/peliculas",
                    ),
                    align="center",
                    mb="8",
                ),

                # Stats
                rx.grid(
                    _stat_card(
                        "Total Películas",
                        rx.text(MovieState.dashboard_stats["total_movies"]),
                        "film",
                        "#E50914",
                    ),
                    _stat_card(
                        "Películas Activas",
                        rx.text(MovieState.dashboard_stats["active_movies"]),
                        "check-circle",
                        "#22c55e",
                    ),
                    _stat_card(
                        "Inactivas",
                        rx.text(MovieState.inactive_movies),
                        "eye-off",
                        "#f59e0b",
                    ),
                    columns="3",
                    spacing="4",
                    mb="8",
                ),

                # Últimas películas
                rx.box(
                    rx.heading(
                        "Últimas películas agregadas",
                        color="white",
                        size="5",
                        mb="4",
                    ),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Película"),
                                rx.table.column_header_cell("Género"),
                                rx.table.column_header_cell("Estado"),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                MovieState.dashboard_stats["recent_movies"],
                                _movie_row,
                            )
                        ),
                        width="100%",
                        variant="surface",
                    ),
                    bg="#111",
                    border="1px solid #222",
                    border_radius="12px",
                    p="6",
                ),
                max_width="1200px",
                mx="auto",
                px="6",
                py="8",
            ),
            min_height="100vh",
            bg="#0a0a0a",
        )
    )
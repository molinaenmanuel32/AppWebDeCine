# cinemax/pages/admin/movies.py
"""
Página de Gestión de Películas — CRUD completo.
Solo accesible para admins.
"""

import reflex as rx
from ...states.movie_state import MovieState
from ...states.app_state import AppState
from ...components.navbar import navbar
from .dashboard import admin_guard


# ── Formulario ────────────────────────────────────────────────────────────────
def _field(label: str, component: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(label, color="#aaa", font_size="0.85rem", font_weight="600"),
        component,
        align="start",
        spacing="1",
        width="100%",
    )


def _input(placeholder: str, value, on_change, type_: str = "text") -> rx.Component:
    return rx.input(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        type=type_,
        bg="#1a1a1a",
        border="1px solid #333",
        color="white",
        _focus={"border_color": "#E50914", "outline": "none"},
        _placeholder={"color": "#555"},
        width="100%",
    )


def movie_form() -> rx.Component:
    return rx.cond(
        MovieState.show_form,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.heading(
                            rx.cond(MovieState.is_editing, "Editar Película", "Nueva Película"),
                            color="white", size="5",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon("x", size=16),
                            on_click=MovieState.close_form,
                            variant="ghost", color="#888", size="1",
                        ),
                        width="100%",
                    ),
                    rx.separator(color="#222"),

                    # Error / success
                    rx.cond(
                        MovieState.form_error != "",
                        rx.callout(MovieState.form_error, color="red", icon="triangle-alert"),
                        rx.fragment(),
                    ),

                    # Campos — 2 columnas
                    rx.grid(
                        _field("Título *", _input("Título de la película",
                               MovieState.form_title,
                               MovieState.set_form_title)),
                        _field("Género", _input("Ej: Acción, Drama",
                               MovieState.form_genre,
                               MovieState.set_form_genre)),
                        _field("Duración (min)", _input("120",
                               MovieState.form_duration,
                               MovieState.set_form_duration, "number")),
                        _field("Clasificación", _input("G, PG, PG-13, R, NC-17",
                               MovieState.form_classification,
                               MovieState.set_form_classification)),
                        _field("Director", _input("Nombre del director",
                               MovieState.form_director,
                               MovieState.set_form_director)),
                        _field("Fecha de estreno", _input("",
                               MovieState.form_release_date,
                               MovieState.set_form_release_date, "date")),
                        _field("Precio (RD$)", _input("350.00",
                               MovieState.form_price,
                               MovieState.set_form_price, "number")),
                        _field("Poster URL", _input("https://...",
                               MovieState.form_poster_url,
                               MovieState.set_form_poster_url)),
                        columns="2",
                        spacing="4",
                        width="100%",
                    ),

                    _field("Trailer URL", _input("https://youtube.com/...",
                           MovieState.form_trailer_url,
                           MovieState.set_form_trailer_url)),

                    _field("Descripción",
                        rx.text_area(
                            placeholder="Sinopsis de la película...",
                            value=MovieState.form_description,
                            on_change=MovieState.set_form_description,
                            bg="#1a1a1a",
                            border="1px solid #333",
                            color="white",
                            rows="3",
                            width="100%",
                            _focus={"border_color": "#E50914"},
                        )
                    ),

                    rx.hstack(
                        rx.checkbox(
                            "Película activa",
                            checked=MovieState.form_active,
                            on_change=MovieState.set_form_active,
                            color_scheme="red",
                        ),
                        rx.spacer(),
                        rx.button(
                            "Cancelar",
                            on_click=MovieState.close_form,
                            variant="outline",
                            color_scheme="gray",
                        ),
                        rx.button(
                            rx.icon("save", size=16),
                            "Guardar",
                            on_click=MovieState.save_movie,
                            bg="#E50914",
                            color="white",
                            _hover={"bg": "#b0060f"},
                        ),
                        width="100%",
                        align="center",
                    ),
                    spacing="4",
                    width="100%",
                ),
                bg="#111",
                border="1px solid #333",
                border_radius="16px",
                p="8",
                max_width="800px",
                width="90%",
                max_height="90vh",
                overflow_y="auto",
            ),
            position="fixed",
            top="0", left="0",
            width="100vw", height="100vh",
            bg="rgba(0,0,0,0.8)",
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="200",
        ),
        rx.fragment(),
    )


# ── Fila de película ──────────────────────────────────────────────────────────
def movie_row(movie: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.image(
                src=rx.cond(
                    movie["poster_url"],
                    movie["poster_url"],
                    "https://via.placeholder.com/50x75?text=N/A",
                ),
                width="50px",
                height="75px",
                object_fit="cover",
                border_radius="6px",
            )
        ),
        rx.table.cell(
            rx.vstack(
                rx.text(movie["title"], color="white", font_weight="600"),
                rx.text(movie["director"] or "", color="#666", font_size="0.8rem"),
                spacing="0",
                align="start",
            )
        ),
        rx.table.cell(rx.text(movie["genre"] or "—", color="#888")),
        rx.table.cell(
            rx.text(
                rx.cond(movie["duration"], f"{movie['duration']} min", "—"),
                color="#888",
            )
        ),
        rx.table.cell(rx.badge(movie["classification"] or "—", variant="outline")),
        rx.table.cell(
            rx.badge(
                rx.cond(movie["active"], "Activa", "Inactiva"),
                color_scheme=rx.cond(movie["active"], "green", "red"),
                variant="soft",
            )
        ),
        rx.table.cell(
            rx.text(
                rx.cond(movie["release_date"], str(movie["release_date"]), "—"),
                color="#888", font_size="0.85rem",
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.icon_button(
                    rx.icon("pencil", size=14),
                    on_click=MovieState.open_edit_form(movie),
                    variant="ghost",
                    color_scheme="blue",
                    size="1",
                    title="Editar",
                ),
                rx.icon_button(
                    rx.icon(
                        rx.cond(movie["active"], "eye-off", "eye"),
                        size=14,
                    ),
                    on_click=MovieState.toggle_status(movie["id"], movie["active"]),
                    variant="ghost",
                    color_scheme=rx.cond(movie["active"], "orange", "green"),
                    size="1",
                    title=rx.cond(movie["active"], "Desactivar", "Activar"),
                ),
                rx.icon_button(
                    rx.icon("trash-2", size=14),
                    on_click=MovieState.delete_movie(movie["id"]),
                    variant="ghost",
                    color_scheme="red",
                    size="1",
                    title="Eliminar",
                ),
                spacing="1",
            )
        ),
        _hover={"bg": "#111"},
    )


@rx.page(route="/admin/peliculas", title="Gestión de Películas",
         on_load=MovieState.admin_load_movies)
def admin_movies_page() -> rx.Component:
    return admin_guard(
        rx.box(
            navbar(),
            movie_form(),
            rx.box(
                # Header
                rx.hstack(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("film", color="#E50914", size=24),
                            rx.heading("Gestión de Películas", color="white", size="6"),
                            spacing="3", align="center",
                        ),
                        rx.text(
                            f"{rx.foreach(MovieState.admin_movies, lambda _: '')} películas en catálogo",
                            color="#888", font_size="0.9rem",
                        ),
                        align="start", spacing="1",
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.link(
                            rx.button(
                                rx.icon("layout-dashboard", size=16),
                                "Dashboard",
                                variant="outline",
                                color_scheme="gray",
                            ),
                            href="/admin",
                        ),
                        rx.button(
                            rx.icon("plus", size=16),
                            "Nueva Película",
                            on_click=MovieState.open_create_form,
                            bg="#E50914",
                            color="white",
                            _hover={"bg": "#b0060f"},
                        ),
                        spacing="3",
                    ),
                    align="center",
                    mb="6",
                ),

                # Tabla
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Poster"),
                                rx.table.column_header_cell("Título"),
                                rx.table.column_header_cell("Género"),
                                rx.table.column_header_cell("Duración"),
                                rx.table.column_header_cell("Clasificación"),
                                rx.table.column_header_cell("Estado"),
                                rx.table.column_header_cell("Estreno"),
                                rx.table.column_header_cell("Acciones"),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(MovieState.admin_movies, movie_row)
                        ),
                        width="100%",
                        variant="surface",
                    ),
                    overflow_x="auto",
                    bg="#111",
                    border="1px solid #222",
                    border_radius="12px",
                ),

                max_width="1400px",
                mx="auto",
                px="6",
                py="8",
            ),
            min_height="100vh",
            bg="#0a0a0a",
        )
    )

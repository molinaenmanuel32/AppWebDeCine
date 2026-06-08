"""
styles/theme.py
Tema global cinematográfico oscuro para Cinemax.
Paleta: negro profundo, rojo cine, gris premium, blanco elegante.
"""

# ─── PALETA PRINCIPAL ────────────────────────────────────────────────
BLACK_DEEP    = "#0a0a0a"
BLACK_CINEMA  = "#0f0f0f"
GRAY_DARK     = "#1a1a1a"
GRAY_MID      = "#2a2a2a"
GRAY_LIGHT    = "#3a3a3a"
GRAY_MUTED    = "#888888"
RED_CINE      = "#e50914"
RED_HOVER     = "#f40612"
RED_DARK      = "#b20710"
GOLD_VIP      = "#f5c518"
GOLD_DARK     = "#d4a017"
WHITE         = "#ffffff"
WHITE_SOFT    = "#e5e5e5"
WHITE_MUTED   = "#a0a0a0"

# ─── FUENTES ─────────────────────────────────────────────────────────
FONT_HEADING  = "Bebas Neue, Impact, sans-serif"
FONT_BODY     = "DM Sans, Helvetica Neue, sans-serif"
FONT_MONO     = "JetBrains Mono, monospace"

# ─── ESTILOS BASE ─────────────────────────────────────────────────────
BASE_STYLE = {
    "font_family": FONT_BODY,
    "background_color": BLACK_CINEMA,
    "color": WHITE_SOFT,
    "min_height": "100vh",
}

# ─── COMPONENTES REUTILIZABLES ────────────────────────────────────────

NAV_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "right": "0",
    "z_index": "1000",
    "padding": "0 2rem",
    "height": "64px",
    "display": "flex",
    "align_items": "center",
    "justify_content": "space-between",
    "transition": "all 0.3s ease",
    "background": f"linear-gradient(180deg, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0) 100%)",
    "backdrop_filter": "blur(10px)",
}

NAV_SCROLLED_STYLE = {
    **NAV_STYLE,
    "background": f"rgba(10,10,10,0.97)",
    "box_shadow": "0 2px 20px rgba(0,0,0,0.8)",
}

HERO_STYLE = {
    "width": "100%",
    "min_height": "90vh",
    "position": "relative",
    "overflow": "hidden",
    "display": "flex",
    "align_items": "end",
    "padding": "0 4rem 5rem",
}

CARD_STYLE = {
    "background": GRAY_DARK,
    "border_radius": "12px",
    "overflow": "hidden",
    "cursor": "pointer",
    "transition": "all 0.3s ease",
    "position": "relative",
    "_hover": {
        "transform": "scale(1.05) translateY(-8px)",
        "box_shadow": f"0 20px 60px rgba(0,0,0,0.8), 0 0 30px rgba(229,9,20,0.3)",
        "z_index": "10",
    },
}

GLASS_STYLE = {
    "background": "rgba(255,255,255,0.05)",
    "backdrop_filter": "blur(12px)",
    "border": "1px solid rgba(255,255,255,0.1)",
    "border_radius": "16px",
}

BUTTON_RED_STYLE = {
    "background": RED_CINE,
    "color": WHITE,
    "border": "none",
    "border_radius": "8px",
    "padding": "12px 28px",
    "font_size": "15px",
    "font_weight": "600",
    "cursor": "pointer",
    "transition": "all 0.2s ease",
    "_hover": {
        "background": RED_HOVER,
        "transform": "translateY(-2px)",
        "box_shadow": f"0 8px 24px rgba(229,9,20,0.5)",
    },
}

BUTTON_OUTLINE_STYLE = {
    "background": "transparent",
    "color": WHITE,
    "border": f"2px solid rgba(255,255,255,0.5)",
    "border_radius": "8px",
    "padding": "12px 28px",
    "font_size": "15px",
    "font_weight": "600",
    "cursor": "pointer",
    "transition": "all 0.2s ease",
    "_hover": {
        "border_color": WHITE,
        "background": "rgba(255,255,255,0.1)",
    },
}

BADGE_VIP_STYLE = {
    "background": f"linear-gradient(135deg, {GOLD_VIP}, {GOLD_DARK})",
    "color": "#1a1200",
    "font_size": "11px",
    "font_weight": "800",
    "padding": "3px 10px",
    "border_radius": "20px",
    "text_transform": "uppercase",
    "letter_spacing": "1",
    "box_shadow": f"0 2px 12px rgba(245,197,24,0.5)",
}

BADGE_CATEGORY_STYLE = {
    "background": "rgba(255,255,255,0.12)",
    "color": WHITE_SOFT,
    "font_size": "11px",
    "padding": "3px 10px",
    "border_radius": "20px",
    "border": "1px solid rgba(255,255,255,0.15)",
}

INPUT_STYLE = {
    "background": GRAY_DARK,
    "border": f"1px solid {GRAY_LIGHT}",
    "border_radius": "10px",
    "color": WHITE,
    "padding": "12px 18px",
    "font_size": "15px",
    "transition": "all 0.2s ease",
    "_focus": {
        "border_color": RED_CINE,
        "box_shadow": f"0 0 0 3px rgba(229,9,20,0.2)",
        "outline": "none",
    },
    "_placeholder": {
        "color": GRAY_MUTED,
    },
}

SECTION_TITLE_STYLE = {
    "font_family": FONT_HEADING,
    "font_size": "2.2rem",
    "letter_spacing": "1",
    "color": WHITE,
    "margin_bottom": "0.25rem",
}

SECTION_ACCENT_STYLE = {
    "width": "48px",
    "height": "4px",
    "background": RED_CINE,
    "border_radius": "2px",
    "margin_bottom": "1.5rem",
}
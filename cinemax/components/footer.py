"""
components/footer.py
Footer cinematográfico premium y responsive.
"""

import reflex as rx
from cinemax.pages.styles.theme import *


def social_icon(icon_name: str, href: str, label: str = "") -> rx.Component:
    return rx.link(
        rx.box(
            rx.icon(icon_name, size=16),
            width="38px",
            height="38px",
            border_radius="50%",
            border="1.5px solid rgba(255,255,255,0.18)",
            background="rgba(255,255,255,0.05)",
            display="flex",
            align_items="center",
            justify_content="center",
            color=WHITE_MUTED,
            transition="all 0.25s ease",
            _hover={
                "background": RED_CINE,
                "border_color": RED_CINE,
                "color": WHITE,
                "transform": "translateY(-3px)",
                "box_shadow": f"0 6px 20px rgba(229,9,20,0.35)",
            },
        ),
        href=href,
        is_external=True,
        aria_label=label,
        text_decoration="none",
    )


def footer_link(label: str, href: str) -> rx.Component:
    return rx.link(
        label,
        href=href,
        color=WHITE_MUTED,
        font_size="13px",
        text_decoration="none",
        transition="color 0.2s ease",
        _hover={"color": WHITE_SOFT},
    )


def footer() -> rx.Component:
    return rx.box(
        rx.box(
            rx.flex(
                # Brand
                rx.vstack(
                    rx.hstack(
                        rx.text("K", color=RED_CINE, font_size="1.8rem", font_family=FONT_HEADING, display="inline"),
                        rx.text("ANKYCINE", color=WHITE, font_size="1.8rem", font_family=FONT_HEADING, display="inline"),
                        spacing="0",
                    ),
                    rx.text(
                        "La mejor experiencia cinematográfica de República Dominicana.",
                        color=WHITE_MUTED,
                        font_size="13px",
                        max_width="240px",
                        line_height="1.6",
                    ),
                    rx.hstack(
                    rx.link(
    rx.image(
        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUJxiJCf8DG8a-_oFjLqIU7Y2AMXggRdgotA&s",
        width="25px",
        height="25px",
        object_fit="cover",
        border_radius="50px",
        flex_shrink="0",
    ),
    href="https://facebook.com",
    is_external=True,
),
               rx.link(
    rx.image(
        src="https://e7.pngegg.com/pngimages/771/708/png-clipart-computer-icons-logo-instagram-logo-miscellaneous-text.png",
        width="25px",
        height="25px",
        object_fit="cover",
        border_radius="5px",
        flex_shrink="0",
    ),
    href="https://instagram.com",
    is_external=True,
),

rx.link(
    rx.image(
        src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAflBMVEUAAAD////19fX5+fmPj49VVVW4uLjv7++cnJy8vLzi4uLt7e1paWktLS2kpKTa2tro6OisrKzQ0NDCwsKCgoI6OjokJCQSEhJ5eXlaWlrMzMxvb29FRUUyMjKjo6OIiIgLCwthYWEbGxtNTU2Xl5cnJydISEh1dXU3NzcXFxcyuDVrAAAPJUlEQVR4nM1da0PqOhAsr4IgQlFABKHgOdfj//+Dl4JAH7ubmTQV56vYZNpk39lErabRaU8ekm33szcfLw7LNEqXh8V43vvsbpOHSbvT+PhRg88eDePd4zyyMX/cxcNRg7NoiuEkXm+WDnI3LDfreNLQTJpgONn2UpjcDWlv2wTL0Az78asHuRte437gGQVlOE1WteidsUqmIScVjmE76QWgd0YvaQebVyiGs3UwemesZ4FmFoRhf/AemF+G90GQLRmA4aSebLHwGkC41mY4CyFcdKxqL9aaDN82jfLLsHm7I8NZOOlpoVfrO9ZgOPkZfieONfajN8P+54/xy/DpLVc9GXYGP8ovw8DT0fJj+Dz+cYJRNH7+MYad0PYLirXPZ/RgGN+JX4aHH2DY39+RYBTtaYnDMnzGHfdm8MXuRpLhy535ZXhpkOHwHiK0ivGwKYYP96Z2BSNwCIbde/PKodsAw87HvVkV0INVI8pwurg3pxIWaLgKZDi7t5KoYgn6VBjD3yNj8sDkDcTw6d5cFDyFYvjznhKKQRiGv0lLlAFoDTfD32Co6XCbcE6Gv5sgQNHF8Dcv0TNcC9XB8PcKmRsc4sZm+FvVRBG20jAZ/k5FX4Wp+i2Gs3vPHIZlwBkMp7/PFtWwNMxwnWHnt3kTFha6M6UzDJ+VSP/OP3qr/RGr3mYcdoX0eIYhFeHHy59kNh318xVQ7f5o+pZ096FWiqoWNYaBxOjy8enN4Y133p6ChGA1gaowHAYYcv76AJeNTJJV7VWrROAUhrXDhqstFfI7ov9cM183ZhjWNLc3iV+2rx3XEm+yES4yfK4zzle3TknTtJv6Dy0G/CWG/S//Qf6L61aMdp68i3O+pKUjMfQXbb2adRPfiP96jr/HGHoriv/CFU8mnlMQVEaVYcfz4XO/JLSGnd8sqnukytAzhQ1F9hgMvYqt1m6GfnL0sYlKba90emUllRl2vHR92AV6Rd8jGzQur9MyQ5/ADJ9bh+ExnXLYpsSw70EQCTx7Y5bS8ym97xJDDzETqpZXQd91YKOCT4vhhOY3b26FXkC/9aJaLjKkDd9986d6eNVY9PcLDN9YglXt0whYeVPYOAWG7Cd8JWY5eouTbXf38rrrPiXxjNOfW25ehY+YZ8h+wh02vf5ssBaiMe+vTxP4VAUZfM87AHmGpNSCvuCsay2M5T4BQwF/qKltZIZkiHvvntbkBbCQNtj5GE7c5HZijiFn6X64ptRJYC9vjbhdj8zsVhJDThe+O158n4u3IscqqE10e2c3htzJF3v7dLhtk2HtjO5QFuVNSERe/+8oZYkP1MO+4aw6oBy7q611ZUhpVTN5Pv2PY3bFwrUdmZV/9QeuDJkA19yahm+IpTAtBcQZpPcyQ0pVGO+6Q4m8Chwlh0yy4SK7LgwZA/6PPoXaJYzvtjlHSLCLzfzNsE1MQskPZKBNdwH2ZiQ2U7vAkNk8uuoKcxLDVI3EO0wKDAmvQveY6siYHFJT1+IB+V6e4ZSYgKqZAxE8UrSUPyFspjmGxORUvVwrYVXEwZKoeJYxyTEkjG7NHuVDPAYeDYYj+CmrG0PCYtM+YTvleRhIDIq4YutfGRIyUFs/oc8qGDoD34nxlSHuVmgGafAaxn/GR4T31OuVIT6wIsiDbsIzDBMVT3BeGOLz2ytjenlLDuihZjx7NPlmiMfqlBxTI4XERqALjtlsvxnCBs1CVhW2vbAfzIbT6XCSfJI1QbppAy+63jfDFP0H5bVaOnibW2wdzm413Gx0V6Rnhvg2lG1iw7WsaE+qFEnfibATNTkxxN+sPJwqvP8JSo0xXnVxCvvr8YkhbCPIi1RdArK/TsTnU5UhrN/WJ4Zw8EOWpFrYYq9Mjogm6J4i+pBNxnAEizjxm2g2rVq028ZFqi5rUAW3HB0Zwmbef+JYir021mPiuIW3UJ8BS8fhkSEsaGS3Qom1G5ZzP0VH1J8CL4T4yBA2EMRtqLxMM36NBxy36jNQK2V3ZAiPJ8b5ZIPNOBzQYtTTXn0G6uk/HhmiKZ1/4qzlCH5sESSiQpUCpytQpTNvRXApovg+ZUlqRFRPQIc0wl5wVLETwbFgUXTLC86KQWTAA+NqwRwsTNsR/FNx5cliypW2xkMequE2TcEnTCLYYRYNDHETW5GyE/DQnlruAZ/KeohgU1jUTeIvnbWYeIRdf1loAiOJUPsnlZSFbA+5CBJpwI36DFQFbCM0AiFaUGKc21mlQYR1/qrPQPdyN0JV57s0jLjE3V0AwCEzqM9AV/pnhP5SzGyLvrat7ltMXN5giEqrXoSuZ3HtiQvAWTbC5FHVh6BZtnmExh5Ff098kc6aWiaSUZvhOEL1ykoaRtruf51laswpPPUh6CpdRKhcEzWTJPbdovQfOGQG9SGo/DhEqCu5RxmKHzsPJuGsM0S1xTJKwV+K+1B6keKryINJFh/Up6ASMoXHEheftN2dVikTFRa18Al42UkK/k7Uh5LM2LsYMslU/Zg9WryawgxFr1bS+PqkzmD0vZ6Ags+5LiP0l1+SEpAcYN1Y1v9Hheo9wTHQA6wtxGSXZJ0YkdITqCMwqgcMO+4L2KYRPWAxTOOwadDxTlDjIbDlN45gX00cTPqhbZdyJwLUkDCc4JnDvoW86aVgq+3icxlx9W3B5SO9CA4IizJSykEY5actsqjhXY2XwgV8nxGsf1Npf0kb3jzuxbUUUS3ADmzbdiM8EyTtiY7wSZYWQ+6MlqoOcaW6xWNtsuSWrBpL1HDVYWq4AJdXCR4vlZeM9O9GyJvyKwxRii+Fh4iQ3tJQbWGZyqnUE7h6Ez1DipsNEzxvoagBSWzry5Q707tXn4N3X2njuSdFSErSVO0gwRwJiIzlTljvHTx/GCkOt2AUqWdqyNMKat0XLh7nTA5YWaaCy37QTFPumKTu4ONzfmTy+JoCripf1UXEh8qgG0f4M3ZMLUakLJvqR9SmRvZIUxcpIf+zWgymvleeesVG1HopcSey9UJownrP6mlGKf77L9ESrnwazQfmDBq9cA8XjqeaKOZQnyK/S6JNC5CRJxbUU2zEqttwtYlHfMljFtepll7jdIXuohCycU3Wl0baR2wXbAztkDDn/OqFiUQbpJisEY60nViM8mrbkGq7oYfsmKVwrhHmtJS8BPOfR6sXogKlRukfcUjru86bbGkiaqm8kaFVhVJrRY8rMy/qUqvPqSnJsOnkM1iavUztd/0TMpbf5bwFeaZHYFDQiJrvxJyN0o+TUO7J5cwMaS4KFPIutxofI85hH0JUGEe3c09sr6mqmMvrQzW7RsxNL+doM8fhb2fX2DPYlTWU/6Pq/uKjGGlkKlZ3O39I96ErmYyFjazKCNiz+KtXGHONOW9nSMnmO1F5GeXtUv2UMpzyM6rgKRc6dw7Y46B5gWJ+GxqlGGAk3qip4oKR+bPcZBizPI/87q999tNqhMr1/82fx/c5qHwz3wrb0OokjOTerbwO1/+30FPBqx/C40VpFf7ZmCAyQ4sgpSnKfTHIQOYZh+/YW16d6uUhGZwWsFnXSN7hXuxtwvUKu2KVmeGFkmu7uNT1FczOLWRbilJ/Gu/OMp9vo8KrddR4D60E6dqscWCVdrnHEFyB44CrMFG/ynTpeDlk28pKn6hAXRGsVghnaI2k/jg6obJNTKu9vnw6CFeB3GT7Vg3ujfVDat+g2xdV+7WxkkqGs8b7zLHQ7fOj624pSF/MJPTcC9PbAr22oz1Jdi+vLy/dZIL0ah2m7ESkvokhLgfSq0NqYUr33RB7X4a4ostZW+qFPt9YRO5fSoX3ZbiO5XnBo8ud0oM2QD+5cBdc3DD0aOOn9RGuvRPNWiFP+Lx2tRd07Y+ohHGnTFfsErza+On9vOt+REVvz0yn0YTXtUxGT/a6OlEh0gVOCokY+ck+q68+dWCnCmWiH8hRIQGebQrNuxHqWadKQuzkXf+jr2nxu2cmct1vQfY+L0Lxfs+e65K8h827u5bjjpJWx/vCLNX7vfg9jDmQeN+k57xnpo7GUPbadbI98EK2jvedXRFwV5D3fU/qNsxv7S4gcKaDOuEG4L4nv7BbBkWvF3R22nXojeea91kid3Z537umlGCU18T+WXOx+rH3+rlA8MAlHebZklsRlsKaWyfD0nIdDZMX+lKgKvbC+BJDpg7sBiUWrJhJi966mzw8vz3E2916FYBcBvj+Q791qni/wfonA4DvsPQzeBV1V68LPQXiHlKvu2Rl77cdKNIMgLpL1uc+YPlBDXSn1cDdB8xvRcX7Dd5gWAV5pzNv+Sreb5ALqRHQ93LT/r4St26GThUed6vjnZjOkB8SIAYLwWiBZ2Sl4XZaGZSzTnXcTQJLw2ux8u6MI6UknZgmHzVgpXbqVhZcINeIePspHMy7mezGXLjJJev7gDdCGLCvIna0HoP3kRxoqnkLPQbHFUqu5mqgWlzKjm0gn8GEq7WYs30clj+XW3962H40nHl1d4M8aKXJFaHkzZM+cBcOuBlCC1V2Dn1jujjc3e8Qhoj1LB7hCVPeYQG5ThphCJQei3G2xt176MZ6iKFb9Yudcpo2aOxLGDmGTgta2g8NS9IleCE4yNBVLiCVhTar7hdgigBm2OqY/qLAsFmb1HFRog9DW/cLDMmbpjkAWsKDoSVvBIZNyhlMxvAMW0M1uVh9pw26FWMq2Uox1AsYq9qifoGVBqTC059h61lOzlZGDXFfp4gvZy/tmgxbIzE+WLFpmvqEe7puhWYoC5yyXdpUjI0RMf4MW+1qtqXsWzTzCdc+5as+DI+7sSxU98W/+6aRTYzZHViHYeXy9FLIuYnoxcCz/tiT4VHiFHLu88LwDbhNn36VcXUYtlqTnKVaPJrsXe6joVejNLcGw6PSu3HMRxNDW6Q90E9qgOGR42XH5XwZ7qyuExvv4tQgDI+a7/wdc8soqF+4qvX9MtRmeNyPWVHqTRWHzGu/kgWNEgIwbLX6g69b1CvAwZQz3gfe8jOPIAyPuE4mlLJf116e3wjF8PbAEOglPlXTyoSCPekM9piggFWCBpkghGbYj+sVw7/GQTZfDsFX6RGTrZe0SXvbJk4VNcEwwyxZEx7UcrOOm2CXoSmGGaaTePfocjPmj7t4SB9VINAkwzM67dlDMnh57G3Gh680jdLlYTGe9z672+Rh0m7mSGYe/wM6Cb1ec3G26QAAAABJRU5ErkJggg==",
        width="25px",
        height="25px",
        object_fit="cover",
        border_radius="5px",
        flex_shrink="0",
    ),
    href="https://pinterest.com",
    is_external=True,
),

rx.link(
    rx.image(
        src="data:image/png;base64,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",
        width="25px",
        height="25px",
        object_fit="cover",
        border_radius="5px",
        flex_shrink="0",
    ),
    href="https://twitter.com",
    is_external=True,
),
                    )

                ),
                

                # Quick links
                rx.vstack(
                    rx.text("Navegación", color=WHITE, font_size="13px", font_weight="700", text_transform="uppercase", letter_spacing="1", margin_bottom="0.5rem"),
                    footer_link("Inicio", "/"),
                    footer_link("Cartelera", "/catalogo"),
                    footer_link("VIP Premium", "/#vip"),
                    footer_link("Promociones", "/#promo"),
                    footer_link("Reservas", "/reservas"),
                    spacing="2",
                    align_items="start",
                ),

                # Account links
                rx.vstack(
                    rx.text("Mi Cuenta", color=WHITE, font_size="13px", font_weight="700", text_transform="uppercase", letter_spacing="1", margin_bottom="0.5rem"),
                    footer_link("Iniciar Sesión", "/login"),
                    footer_link("Registrarse", "/registro"),
                    footer_link("Mis Reservas", "#"),
                    footer_link("Perfil VIP", "#"),
                    spacing="2",
                    align_items="start",
                ),

                # Contact
                rx.vstack(
                    rx.text("Contacto", color=WHITE, font_size="13px", font_weight="700", text_transform="uppercase", letter_spacing="1", margin_bottom="0.5rem"),
                    rx.hstack(rx.icon("map-pin", size=14, color=GRAY_MUTED), rx.text("Santo Domingo, RD", color=WHITE_MUTED, font_size="13px"), spacing="2"),
                    rx.hstack(rx.icon("phone", size=14, color=GRAY_MUTED), rx.text("+1 (809) 555-0100", color=WHITE_MUTED, font_size="13px"), spacing="2"),
                    rx.hstack(rx.icon("mail", size=14, color=GRAY_MUTED), rx.text("info@kankycine.com.do", color=WHITE_MUTED, font_size="13px"), spacing="2"),
                    spacing="2",
                    align_items="start",
                ),

                gap="3rem",
                flex_wrap="wrap",
            ),

            rx.divider(border_color="rgba(255,255,255,0.08)", margin="2.5rem 0 1.5rem"),

            rx.flex(
                rx.text("© 2025 KankyCine Premium. Todos los derechos reservados.", color=GRAY_MUTED, font_size="12px"),
                rx.hstack(
                    footer_link("Términos de uso", "#"),
                    rx.text("·", color=GRAY_MUTED, font_size="12px"),
                    footer_link("Política de privacidad", "#"),
                    rx.text("·", color=GRAY_MUTED, font_size="12px"),
                    footer_link("Cookies", "#"),
                    spacing="2",
                    align_items="center",
                ),
                justify="between",
                flex_wrap="wrap",
                gap="1rem",
                align_items="center",
            ),

            max_width="1200px",
            margin="0 auto",
            padding="3rem 2rem",
        ),

        background=BLACK_DEEP,
        border_top="1px solid rgba(255,255,255,0.06)",
        width="100%",

)
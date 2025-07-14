import arcade
from arcade.color import * # type: ignore
from PIL import Image, ImageDraw, ImageFont

VER = "v0.2"
WINDOW_TITLE = f"Irisis {VER}"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

GRAPH_WIDTH = 100
GRAPH_HEIGHT = 60

button_font = "BoutiqueBitmap9x9 1.9"
DEFAULT_BUTTON_STYLE = \
{
    "normal": {
        "font_size": 23,
        "font_name": button_font,
        "font_color": WHITE,
        "bg": (31, 30, 51, 255),
        "border": (1, 1, 1, 1),
        "border_width": 1
    },
    "hover": {
        "font_size": 23,
        "font_name": button_font,
        "font_color": WHITE,
        "bg": (62, 60, 101, 255),
        "border": (1, 1, 1, 1),
        "border_width": 1
    },
    "press": {
        "font_size": 23,
        "font_name": button_font,
        "font_color": QUEEN_PINK,
        "bg": (11, 12, 18, 255),
        "border": (1, 1, 1, 1),
        "border_width": 1
    },
}
WARN_BUTTON_STYLE = \
{
    "normal": {
        "font_size": 23,
        "font_name": button_font,
        "font_color": WHITE,
        "bg": (31, 30, 51, 255),
        "border": (1, 1, 1, 1),
        "border_width": 1
    },
    "hover": {
        "font_size": 23,
        "font_name": button_font,
        "font_color": WHITE,
        "bg": PUCE_RED,
        "border": (1, 1, 1, 1),
        "border_width": 1
    },
    "press": {
        "font_size": 23,
        "font_name": button_font,
        "font_color": QUEEN_PINK,
        "bg": (28, 12, 13, 255),
        "border": (1, 1, 1, 1),
        "border_width": 1
    },
}

BLOCK_INFO = (
        None,
        ("草", CAL_POLY_GREEN),
        ("土", CAPUT_MORTUUM),
    )

BLOCK_IMG = []
for block_info in BLOCK_INFO:
    if block_info is not None:
        t, c = block_info
        font = ImageFont.truetype("assets/精品點陣體-Bold_1.9.ttf", 30)
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), t, font=font, fill=c)
        BLOCK_IMG.append(img)
    else:
        BLOCK_IMG.append(None)
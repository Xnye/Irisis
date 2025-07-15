import arcade
from arcade.color import * # type: ignore
from PIL import Image, ImageDraw, ImageFont

VER = "v0.3"
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

BLOCK_INFO = {
    -1: ("您", BLACK, WHITE),
    0: ("家", WHITE, 0),
    1: ("草", CAL_POLY_GREEN, 0),
    2: ("土", CAPUT_MORTUUM, 0),
}

# 预渲染材质
BLOCK_TEX = {}
for no in BLOCK_INFO:
    if BLOCK_INFO[no] is not None:
        t, c1, c2 = BLOCK_INFO[no]
        font = ImageFont.truetype("assets/精品點陣體-Bold_1.9.ttf", 30)
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0) if c2 == 0 else c2)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), t, font=font, fill=c1)
        tex = arcade.Texture(img)
        BLOCK_TEX[no] = tex
    else:
        BLOCK_TEX[no] = None
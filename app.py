#!/usr/bin/env python3
import curses
import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from enum import Enum

import ST7789

# Create ST7789 LCD display class.
disp = ST7789.ST7789(
    height=240,
    rotation=90,
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000,
    offset_left=0,
    offset_top=0
)

# State enum
class AppState(Enum):
    HOME = 0
    POKEDEX = 1
    GAME = 2

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height

# Load font
font = ImageFont.truetype('./pokemon_font.ttf', 16)

# OS setting
os.environ.setdefault("ESCDELAY", "15")

def draw_rect_button(img: Image, text: str, loc: tuple[int, int], size: tuple[int, int],
                     fill: tuple[int, int, int] = None):
    draw = ImageDraw.Draw(img)

    # Compute rectangle points
    x1 = int(loc[0] - ((size[0]) / 2))
    x2 = int(loc[0] + ((size[0]) / 2))
    y1 = int(loc[1] - ((size[1]) / 2))
    y2 = int(loc[1] + ((size[1]) / 2))

    # Draw rectangle
    draw.rectangle((x1, y1, x2, y2), outline=(0, 0, 0),
                   fill=(255, 255, 255) if fill is None else fill)

    # Draw text
    draw.text((loc[0], loc[1]), text, (0, 0, 0), font=font, anchor="mm")

def draw_pokemon_entry(img: Image, entry_num: int, loc: tuple[int, int]):
    draw = ImageDraw.Draw(img)
    x1 = int(loc[0] - 50)
    x2 = int(loc[0] + 50)
    y1 = int(loc[1] - 45)
    y2 = int(loc[1] + 45)

    draw.rectangle((x1, y1, x2, y2), outline=(0, 0, 0), fill=(255, 255, 255))

def draw_home(img: Image, sel: int):
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, WIDTH, HEIGHT), (135, 206, 235))
    draw_rect_button(img, "Pokedex", (120, 65), (160, 70), 
                     (211, 211, 211) if sel == 0 else None)
    draw_rect_button(img, "Game", (120, 175), (160, 70),
                     (211, 211, 211) if sel == 1 else None)

def draw_pokedex(img: Image):
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, WIDTH, HEIGHT), (135, 206, 235))
    draw.text((0, 0), "1/200", (0, 0, 0), font=font)
    draw_pokemon_entry(img, 0, (60, 70))
    draw_pokemon_entry(img, 0, (180, 70))
    draw_pokemon_entry(img, 0, (60, 170))
    draw_pokemon_entry(img, 0, (180, 170))


def draw_game(img: Image):
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, WIDTH, HEIGHT), (135, 206, 235))

def main(win):
    # Curses
    win.nodelay(True)

    # Initialize the image to be drawn to the display
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(135, 206, 235))

    # Initialize state
    state = AppState.HOME
    sel = 0
    kinput = None

    while 1:
        # Handle input
        kinput = win.getch()
        if kinput >= 0:
            win.addch(kinput)
            if kinput == ord("w"):
                if sel > 0:
                    sel -= 1
            elif kinput == ord("s"):
                if sel < 1:
                    sel += 1
            elif kinput == curses.KEY_ENTER or kinput == 10 or kinput == 13:
                if sel == 0:
                    state = AppState.POKEDEX
                elif sel == 1:
                    state = AppState.GAME
            elif kinput == 27:
                kinput = win.getch()
                if kinput == -1:
                    state = AppState.HOME
        
        if state is AppState.HOME:
            draw_home(img, sel)
        elif state is AppState.POKEDEX:
            draw_pokedex(img)
        elif state is AppState.GAME:
            draw_game(img)

        # Call to draw to screen
        disp.display(img)

# Main
if __name__ == "__main__":
    curses.wrapper(main)

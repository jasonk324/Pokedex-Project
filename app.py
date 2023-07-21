#!/usr/bin/env python3
import curses
import os
import json

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

class PokedexState(Enum):
    ENTRY0 = 0
    ENTRY1 = 1
    ENTRY2 = 2
    ENTRY3 = 3

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height

# Load font
font = ImageFont.truetype('./pokemon_font.ttf', 16)
name_font = ImageFont.truetype('./pokemon_font.ttf', 10) # Smaller version for pokemon names
GREY = (230, 230, 230)

# OS setting
os.environ.setdefault("ESCDELAY", "15")

# JSON
json_data = None
with open("./Data/Pokemon(wAbilities).json", "r") as json_file:
    json_data = json.load(json_file)

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

def draw_pokemon_entry(img: Image, entry_num: int, loc: tuple[int, int],
                       fill: tuple[int, int, int] = None):
    draw = ImageDraw.Draw(img)

    x1 = int(loc[0] - 50)
    x2 = int(loc[0] + 50)
    y1 = int(loc[1] - 45)
    y2 = int(loc[1] + 45)

    draw.rectangle((x1, y1, x2, y2), outline=(0, 0, 0),
                    fill=(255, 255, 255) if fill is None else fill)

    image_path = "./Data/Images/#" + json_data[entry_num]["top_image"][9:]
    image_file = Image.open(image_path)
    image_file = image_file.resize((60, 60))

    img.paste(image_file, ((loc[0] - 45), (loc[1] - 40)))

    # Text
    draw.text((loc[0] - 45, loc[1] + 30), json_data[entry_num]["name"],
               (0, 0, 0), font=name_font, anchor="lm")

def draw_home(img: Image, state: list, inp: int):
    draw = ImageDraw.Draw(img)

    # Handle passed input, updating state if applicable
    if inp == ord("w"):
        if state[1] > 0:
            state[1] -= 1
    elif inp == ord("s"):
        if state[1] < 1:
            state[1] += 1
    elif inp == curses.KEY_ENTER or inp == 10 or inp == 13:
        if state[1] == 0:
            state[0] = AppState.POKEDEX
            state[1] = PokedexState.ENTRY0
        elif state[1] == 1:
            state[0] = AppState.GAME
            state[1] = 0

    # Refresh
    draw.rectangle((0, 0, WIDTH, HEIGHT), (135, 206, 235))

    # Draw buttons with highlight based on current sel (state[1])
    draw_rect_button(img, "Pokedex", (120, 65), (160, 70), 
                     GREY if state[1] == 0 else None)
    draw_rect_button(img, "Game", (120, 175), (160, 70),
                     GREY if state[1] == 1 else None)

def draw_pokedex(img: Image, state: list, inp: int):
    draw = ImageDraw.Draw(img)

    # Handle passed input, updating state if applicable
    if inp == ord("w"):
        if state[1] is PokedexState.ENTRY2:
            state[1] = PokedexState.ENTRY0
        elif state[1] is PokedexState.ENTRY3:
            state[1] = PokedexState.ENTRY1
    elif inp == ord("s"):
        if state[1] is PokedexState.ENTRY0:
            state[1] = PokedexState.ENTRY2
        elif state[1] is PokedexState.ENTRY1:
            state[1] = PokedexState.ENTRY3
    elif inp == ord("a"):
        if state[1] is PokedexState.ENTRY1:
            state[1] = PokedexState.ENTRY0
        elif state[1] is PokedexState.ENTRY3:
            state[1] = PokedexState.ENTRY2
    elif inp == ord("d"):
        if state[1] is PokedexState.ENTRY0:
            state[1] = PokedexState.ENTRY1
        elif state[1] is PokedexState.ENTRY2:
            state[1] = PokedexState.ENTRY3
    elif inp == curses.KEY_ENTER or inp == 10 or inp == 13:
        pass
    elif inp == 27:
        state[0] = AppState.HOME
        state[1] = 0

    # Refresh
    draw.rectangle((0, 0, WIDTH, HEIGHT), (135, 206, 235))

    draw.text((0, 0), "1/200", (0, 0, 0), font=font)
    draw_pokemon_entry(img, 0, (60, 70),
                       GREY if state[1] is PokedexState.ENTRY0 else None)
    draw_pokemon_entry(img, 1, (180, 70),
                       GREY if state[1] is PokedexState.ENTRY1 else None)
    draw_pokemon_entry(img, 2, (60, 170),
                       GREY if state[1] is PokedexState.ENTRY2 else None)
    draw_pokemon_entry(img, 4, (180, 170),
                       GREY if state[1] is PokedexState.ENTRY3 else None)

def draw_game(img: Image, state: list, inp: int):
    draw = ImageDraw.Draw(img)

    # Handle passed input, updating state if applicable
    if inp == 27:
        state[0] = AppState.HOME
        state[1] = 0

    # Refresh
    draw.rectangle((0, 0, WIDTH, HEIGHT), (135, 206, 235))

def main(win):
    # Curses
    win.nodelay(True)

    # Initialize the image to be drawn to the display
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(135, 206, 235))

    # Initialize state
    state = [AppState.HOME, 0]
    kinput = None

    while 1:
        # Handle input
        kinput = win.getch()
        if kinput >= 0:
            win.addch(kinput)
        else:
            kinput = None
        

        if state[0] is AppState.HOME:
            draw_home(img, state, kinput)
        elif state[0] is AppState.POKEDEX:
            draw_pokedex(img, state, kinput)
        elif state[0] is AppState.GAME:
            draw_game(img, state, kinput)

        # Call to draw to screen
        disp.display(img)

# Main
if __name__ == "__main__":
    curses.wrapper(main)

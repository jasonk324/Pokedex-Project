#!/usr/bin/env python3
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7789

def main():
    # Clear the display to a red background.
    # Can pass any tuple of red, green, blue values (from 0 to 255 each).
    # Get a PIL Draw object to start drawing on the display buffer.
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(135, 206, 235))

    draw = ImageDraw.Draw(img)

    # Draw buttons on main menu
    draw.rectangle((40, 30, 200, 100), outline=(0, 0, 0), fill=(255, 255, 255))
    draw.rectangle((40, 140, 200, 210), outline=(0, 0, 0), fill=(255, 255, 255))

    #draw_rotated_text_centered(img, "Pokedex", (120, 65), 0, font)
    #draw_rotated_text_centered(img, "Game", (120, 165), 0, font)

    draw.text((120, 65), "Pokedex", (0, 0, 0), font=font, anchor="mm")
    draw.text((120, 175), "Game", (0, 0, 0), font=font, anchor="mm")

    # Call to draw to screen
    disp.display(img)

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

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height

# Load font
font = ImageFont.truetype('./pokemon_font.ttf', 16)

# Main
if __name__ == "__main__":
    main()

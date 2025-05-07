import time
import board
import neopixel

# Aantal LED's in de strip
num_pixels = 30
# GPIO pin waar de data-pin van de LED-strip is aangesloten
pixel_pin = board.D18

# Maak een NeoPixel-object aan
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

def set_color(color):
    pixels.fill(color)

try:
    while True:
        set_color((255, 0, 0))  # Rood
        time.sleep(1)
        set_color((0, 255, 0))  # Groen
        time.sleep(1)
        set_color((0, 0, 255))  # Blauw
        time.sleep(1)
        set_color((0, 0, 0))    # Uit
        time.sleep(1)
except KeyboardInterrupt:
    set_color((0, 0, 0))  # Zet de LED's uit bij het stoppen van het script

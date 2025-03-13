import time
import board
import neopixel
import random

# Define the pin and the number of pixels
PIXEL_PIN = board.D18      # Pin D18 where NeoPixel strip is connected
NUM_PIXELS = 89           # Number of pixels in your strip
ORDER = neopixel.GRBW     # RGBW (Red, Green, Blue, White)

# Create NeoPixel object
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, pixel_order=ORDER, auto_write=False)

# F1-style 5 lights simulation (red color for lights)
def f1_5_lights():
    # Turn all LEDs off first
    pixels.fill((0, 0, 0, 0))  # Off (RGBW: 0, 0, 0, 0)
    pixels.show()
    time.sleep(1)  # Wait for 1 second before starting the lights sequence

    # Light up the LEDs in groups and wait 1 second between each group

    # Light up LEDs 5-10
    for i in range(5, 10):
        pixels[i] = (255, 0, 0, 0)  # Red color for the LED
    pixels.show()  # Apply the changes to the strip
    time.sleep(1)  # Wait for 1 second before lighting the next group
    
    # Light up LEDs 22-28
    for i in range(22, 28):
        pixels[i] = (255, 0, 0, 0)  # Red color for the LED
    pixels.show()  # Apply the changes to the strip
    time.sleep(1)  # Wait for 1 second before lighting the next group
    
    # Light up LEDs 42-48
    for i in range(42, 48):
        pixels[i] = (255, 0, 0, 0)  # Red color for the LED
    pixels.show()  # Apply the changes to the strip
    time.sleep(1)  # Wait for 1 second before lighting the next group
    
    # Light up LEDs 62-68
    for i in range(62, 68):
        pixels[i] = (255, 0, 0, 0)  # Red color for the LED
    pixels.show()  # Apply the changes to the strip
    time.sleep(1)  # Wait for 1 second before lighting the next group
    
    # Light up LEDs 80-85
    for i in range(80, 85):
        pixels[i] = (255, 0, 0, 0)  # Red color for the LED
    pixels.show()  # Apply the changes to the strip
    time.sleep(1)  # Wait for 1 second before finishing the sequence

    # Hold all 5 lights on for a short moment
    time.sleep(1)  # Lights are on for 1 second

    # Random delay before turning off all the lights at the end
    random_delay = random.uniform(0.5, 3)  # Random delay between 0.5 and 1 second
    print(f"Random delay before turning off: {random_delay:.2f} seconds")  # For debugging
    time.sleep(random_delay)  # Wait for a random time before turning off the lights

    # Now turn off all the lights quickly
    pixels.fill((0, 0, 0, 0))  # Off (RGBW: 0, 0, 0, 0)
    pixels.show()

# Call the function once to simulate the lights sequence
f1_5_lights()

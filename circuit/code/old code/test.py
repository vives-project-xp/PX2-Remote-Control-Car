import time
import board
import neopixel
import random
import RPi.GPIO as GPIO

# GPIO initialisatie
GPIO.setwarnings(False)
if GPIO.getmode() is not None:
    GPIO.cleanup()
BUTTON_PIN = 7
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# NeoPixel configuratie
pixels = neopixel.NeoPixel(
    board.D18,
    89,
    brightness=0.5,
    pixel_order=neopixel.GRBW,
    auto_write=False
)

def f1_5_lights():
    segments = [(5, 10), (22, 28), (42, 48), (62, 68), (80, 85)]
    
    pixels.fill((0, 0, 0, 0))
    pixels.show()
    time.sleep(1)

    for start, end in segments:
        pixels[start:end] = [(255, 0, 0, 0)] * (end - start)
        pixels.show()
        time.sleep(1)
    
    time.sleep(1)
    time.sleep(random.uniform(0.5, 3))
    
    pixels.fill((0, 0, 0, 0))
    pixels.show()

def main():
    try:
        print("Ready - Druk op de knop (PIN7) om te starten...")
        while True:
            if not GPIO.input(BUTTON_PIN):
                print("Start sequence!")
                f1_5_lights()
                time.sleep(0.5)
                while not GPIO.input(BUTTON_PIN):
                    time.sleep(0.1)
                
    except KeyboardInterrupt:
        print("\nAfsluiten...")
        pixels.fill((0, 0, 0, 0))
        pixels.show()
        GPIO.cleanup()

if __name__ == "__main__":
    main()

import time
import board
import neopixel
import random
import RPi.GPIO as GPIO
import pygame

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

# Audio initialisatie
pygame.mixer.init()

def f1_5_lights(small_beep, long_beep):
    segments = [(5, 10), (22, 28), (42, 48), (62, 68), (80, 85)]
    
    # Reset alle LEDs
    pixels.fill((0, 0, 0, 0))
    pixels.show()
    time.sleep(1)

    # Licht elk segment op met beep
    for start, end in segments:
        pixels[start:end] = [(255, 0, 0, 0)] * (end - start)
        pixels.show()
        small_beep.play()
        time.sleep(1)
    
    # Wacht willekeurige tijd
    time.sleep(1)
    time.sleep(random.uniform(0.2, 0.8))
    
    # Doe lichten uit en speel lange beep
    pixels.fill((0, 0, 0, 0))
    pixels.show()
    long_beep.play()
    time.sleep(long_beep.get_length())  # Wacht tot beep klaar is

def main():
    try:
        # Laad geluidseffecten
        small_beep = pygame.mixer.Sound('smal_Beep.wav')
        long_beep = pygame.mixer.Sound('long_beep.wav')
        
        print("Ready - Druk op de knop (PIN7) om te starten...")
        while True:
            if not GPIO.input(BUTTON_PIN):
                print("Start sequence!")
                f1_5_lights(small_beep, long_beep)
                
                # Wacht tot knop losgelaten is
                time.sleep(0.5)
                while not GPIO.input(BUTTON_PIN):
                    time.sleep(0.1)
                
    except KeyboardInterrupt:
        print("\nAfsluiten...")
        pixels.fill((0, 0, 0, 0))
        pixels.show()
        pygame.mixer.quit()
        GPIO.cleanup()

if __name__ == "__main__":
    main()

import time
import board
import neopixel
import random
import RPi.GPIO as GPIO
import pygame

# GPIO initialisatie
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Knoppen en LED configuratie
BUTTON_PIN = 23    
BUTTON_LED = 26    
RESET_PIN = 25
RESET_LED = 16

# GPIO setup
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(RESET_LED, GPIO.OUT)

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

def update_button_leds():
    """Update LED status gebaseerd op knop status"""
    GPIO.output(BUTTON_LED, not GPIO.input(BUTTON_PIN))  # LED aan wanneer knop ingedrukt
    GPIO.output(RESET_LED, not GPIO.input(RESET_PIN))     # LED aan wanneer knop ingedrukt

def reset_lights():
    pixels.fill((0, 0, 0, 0))
    pixels.show()
    pygame.mixer.stop()
    update_button_leds()

def wait_with_reset(duration):
    start = time.time()
    while time.time() - start < duration:
        update_button_leds()
        if not GPIO.input(RESET_PIN):
            reset_lights()
            return True
        time.sleep(0.05)
    return False

def f1_5_lights(small_beep, long_beep):
    segments = [(5, 10), (22, 28), (42, 48), (62, 68), (80, 85)]
    
    pixels.fill((0, 0, 0, 0))
    pixels.show()
    if wait_with_reset(1):
        return

    for start, end in segments:
        pixels[start:end] = [(255, 0, 0, 0)] * (end - start)
        pixels.show()
        small_beep.play()
        if wait_with_reset(1):
            return
    
    total_wait = 1 + random.uniform(0.2, 0.8)
    if wait_with_reset(total_wait):
        return
    
    pixels.fill((0, 0, 0, 0))
    pixels.show()
    long_beep.play()
    
    start_time = time.time()
    while time.time() - start_time < long_beep.get_length():
        update_button_leds()
        if not GPIO.input(RESET_PIN):
            reset_lights()
            return
        time.sleep(0.1)

def main():
    try:
        small_beep = pygame.mixer.Sound('small_beep.wav')
        long_beep = pygame.mixer.Sound('long_beep.wav')
        
        print("Systeem actief - start: rode knop / reset: witte knop")
        while True:
            update_button_leds()
            
            # Reset functionaliteit
            if not GPIO.input(RESET_PIN):
                reset_lights()
                while not GPIO.input(RESET_PIN):
                    update_button_leds()
                    time.sleep(0.05)
                time.sleep(0.1)
            
            # Start functionaliteit
            if not GPIO.input(BUTTON_PIN):
                f1_5_lights(small_beep, long_beep)
                while not GPIO.input(BUTTON_PIN):
                    update_button_leds()
                    time.sleep(0.05)
                time.sleep(0.1)
            
            time.sleep(0.01)

    except KeyboardInterrupt:
        reset_lights()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
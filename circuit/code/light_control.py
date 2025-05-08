import time
import board
import neopixel
import RPi.GPIO as GPIO
import pygame
import random

class LightControl:
    def __init__(self):
        # GPIO-configuratie
        self.BUTTON_PIN = 23  # GPIO-pin voor de knop
        self.RESET_PIN = 25  # GPIO-pin voor de resetknop
        self.BUTTON_LED = 26  # GPIO-pin voor de LED van de knop
        self.RESET_LED = 16  # GPIO-pin voor de LED van de resetknop

        # Stel GPIO in
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON_LED, GPIO.OUT)
        GPIO.setup(self.RESET_LED, GPIO.OUT)

        # NeoPixel-configuratie
        self.pixels = neopixel.NeoPixel(
            board.D18,
            89,
            brightness=0.5,
            pixel_order=neopixel.GRBW,
            auto_write=False
        )

        # Audio-configuratie
        pygame.mixer.init()
        self.small_beep = pygame.mixer.Sound('small_beep.wav')
        self.long_beep = pygame.mixer.Sound('long_beep.wav')

    def reset_lights(self):
        # Reset alle LEDs naar uitgeschakeld
        self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()
        pygame.mixer.stop()
        self._update_button_leds()

    def start_sequence(self):
        # Definieer de segmenten van de LED-strip die geactiveerd worden
        segments = [(5, 10), (22, 28), (42, 48), (62, 68), (80, 85)]
        
        # Initieel resetten van de LEDs
        self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()
        if self._wait_with_reset(1):
            return

        # Activeer elk segment
        for start, end in segments:
            self.pixels[start:end] = [(255, 0, 0, 0)] * (end - start)
            self.pixels.show()
            self.small_beep.play()
            if self._wait_with_reset(1):
                return

        # Eindsequentie
        if self._wait_with_reset(1 + random.uniform(0.2, 0.8)):
            return
        
        self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()
        self.long_beep.play()
        self._play_long_beep_with_reset()
        
    def _update_button_leds(self):
        # Update de status van de knop-LEDs op basis van de knopstatus
        GPIO.output(self.BUTTON_LED, not GPIO.input(self.BUTTON_PIN))
        GPIO.output(self.RESET_LED, not GPIO.input(self.RESET_PIN))

    def _wait_with_reset(self, duration):
        # Wacht een bepaalde tijd en controleer of de resetknop wordt ingedrukt
        start = time.time()
        while time.time() - start < duration:
            self._update_button_leds()
            if not GPIO.input(self.RESET_PIN):
                self.reset_lights()
                return True
            time.sleep(0.05)
        return False

    def _play_long_beep_with_reset(self):
        # Speel een lange piep af en controleer op reset
        start_time = time.time()
        while time.time() - start_time < self.long_beep.get_length():
            self._update_button_leds()
            if not GPIO.input(self.RESET_PIN):
                self.reset_lights()
                return
            time.sleep(0.1)

    def cleanup(self):
        # Maak de GPIO en LEDs schoon bij afsluiten
        self.reset_lights()
        GPIO.cleanup()
        
if __name__ == "__main__":
    lc = LightControl()
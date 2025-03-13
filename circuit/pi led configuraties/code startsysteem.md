# Code startsysteem

Hier is de code voor het startsysteem dat de leds aanstuurt en via rfid de tijd dat de auto over de ronde deed en welke plaats ze behaald hebben.

Moet nog getest worden.

```python
import time
import board
import neopixel
import pygame
import RPi.GPIO as GPIO
import csv
from mfrc522 import SimpleMFRC522

# --- LED & Buzzer Config ---
LED_COUNT = 5
LED_PIN = board.D18
BRIGHTNESS = 0.5
BUZZER_PIN = 13

# --- GPIO Setup ---
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=BRIGHTNESS, auto_write=False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# --- Button Config ---
START_BUTTON = 21
RESET_BUTTON = 20
GPIO.setup(START_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RESET_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# --- RFID Config ---
reader = SimpleMFRC522()
car_times = {1: [], 2: []}
last_lap = {1: 0, 2: 0}

# --- Pygame Setup ---
pygame.init()
screen1 = pygame.display.set_mode((640, 480), pygame.NOFRAME, display=0)
screen2 = pygame.display.set_mode((640, 480), pygame.NOFRAME, display=1)
font = pygame.font.Font(None, 50)

def buzzer(state: bool):
    GPIO.output(BUZZER_PIN, GPIO.HIGH if state else GPIO.LOW)

def clear_leds():
    pixels.fill((0, 0, 0))
    pixels.show()

def start_lights():
    """Start sequence with LEDs and buzzer."""
    for i in range(LED_COUNT):
        pixels[i] = (255, 0, 0)
        pixels.show()
        buzzer(True)
        time.sleep(0.2)
        buzzer(False)
        time.sleep(0.3)
    time.sleep(3)
    clear_leds()
    buzzer(True)
    time.sleep(1)
    buzzer(False)

def save_lap_time(car_number, lap_time):
    """Save lap times to a CSV file."""
    with open("lap_times.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([car_number, lap_time, time.strftime("%Y-%m-%d %H:%M:%S")])

def update_screen():
    """Update screens with last lap, best lap, and placements."""
    screen1.fill((0, 0, 0))
    screen2.fill((0, 0, 0))

    if car_times[1] and car_times[2]:
        lap1, best1 = car_times[1][-1], min(car_times[1])
        lap2, best2 = car_times[2][-1], min(car_times[2])

        results = sorted([(1, lap1, best1), (2, lap2, best2)], key=lambda x: x[1])
        placements = {results[0][0]: "1st", results[1][0]: "2nd"}

        for screen, (car, last, best) in zip([screen1, screen2], results):
            text = font.render(f"Auto {car} - {placements[car]}: {last:.3f} sec (Best: {best:.3f} sec)", True, (255, 255, 255))
            screen.blit(text, (50, 200))

    pygame.display.flip()

def scan_rfid():
    """Read RFID tags and update lap times."""
    print("Wacht op RFID...")
    id, _ = reader.read()
    timestamp = time.time()
    car_number = 1 if id == 123456789 else 2

    if last_lap[car_number]:
        lap_time = round(timestamp - last_lap[car_number], 3)
        car_times[car_number].append(lap_time)
        print(f"Auto {car_number}: {lap_time} sec")
        save_lap_time(car_number, lap_time)  # Save to CSV

    last_lap[car_number] = timestamp
    update_screen()

def reset_system():
    """Reset the race system."""
    print("Resetting system...")
    global car_times, last_lap
    car_times, last_lap = {1: [], 2: []}, {1: 0, 2: 0}
    clear_leds()
    screen1.fill((0, 0, 0))
    screen2.fill((0, 0, 0))
    pygame.display.flip()
    time.sleep(1)

def main():
    try:
        print("Druk op de startknop om de race te beginnen...")
        while GPIO.input(START_BUTTON) == GPIO.LOW:
            time.sleep(0.1)
        print("Startknop ingedrukt! Startprocedure begint...")
        start_lights()
        
        while True:
            if GPIO.input(RESET_BUTTON) == GPIO.HIGH:
                reset_system()
            scan_rfid()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nAfsluiten...")
        clear_leds()
        GPIO.cleanup()

if __name__ == "__main__":
    main()

```

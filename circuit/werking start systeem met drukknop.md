Laten we vanaf het begin beginnen en alles stap voor stap uitleggen, zodat je een compleet systeem hebt met een F1-startlicht, RFID-timing, en twee aparte schermen met een fysieke start- en resetknop. We zullen de benodigde hardware en code doorlopen.

### Benodigde Hardware:
1. **Raspberry Pi (bijv. Raspberry Pi 4)**
2. **RFID lezer (bijv. MFRC522)**
3. **Adresserbare LED-strips (bijv. WS2812)**
4. **Drukknoppen** voor de **startknop** en de **resetknop**
5. **Buzzer**
6. **2 HDMI-schermen** voor de timing van de auto's
7. **Weerstanden** voor de drukknoppen (meestal 10kΩ)
8. **Jumper draadjes** en een **breadboard** voor de aansluitingen

### Aansluitingen:
1. **RFID Lezer (MFRC522)**:
   - VCC naar 3.3V
   - GND naar GND
   - SDA naar GPIO 8
   - SCK naar GPIO 11
   - MOSI naar GPIO 10
   - MISO naar GPIO 9
   - IRQ (niet nodig)
   - RST naar GPIO 17
   - GND naar GND

2. **Drukknoppen**:
   - **Startknop** naar GPIO 21
   - **Resetknop** naar GPIO 20
   - Beide knoppen naar GND, met een 10kΩ **pull-down weerstand**.

3. **Adresserbare LED's (WS2812)**:
   - Data pin naar **GPIO 18** (of een andere geschikte pin).
   - VCC naar 5V en GND naar GND.

4. **Buzzer**:
   - Positieve pin naar GPIO 13.
   - Negatieve pin naar GND.

---

### Stap 1: Installeren van de benodigde software

Op je Raspberry Pi moet je de volgende bibliotheken installeren voor de juiste werking:

```bash
sudo apt update
sudo apt install python3-pip
sudo pip3 install RPi.GPIO
sudo pip3 install adafruit-circuitpython-neopixel
sudo pip3 install mfrc522
sudo pip3 install pygame
```

### Stap 2: Python-script voor het systeem

Hier is de volledige Python-code die de F1-startlichtsequentie, RFID-timing en het gebruik van twee schermen integreert, inclusief de start- en resetknoppen.

```python
import time
import board
import neopixel
import pygame
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# --- LED & Buzzer Config ---
LED_COUNT = 5  
LED_PIN = board.D18  
BRIGHTNESS = 0.5  
buzzer_pin = 13  

# --- RFID Config ---
reader = SimpleMFRC522()
car_times = {1: [], 2: []}
last_lap = {1: 0, 2: 0}

# --- GPIO Setup ---
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=BRIGHTNESS, auto_write=False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# --- Startknop Config ---
start_button = 21  
GPIO.setup(start_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Pull-down weerstand

# --- Resetknop Config ---
reset_button = 20  
GPIO.setup(reset_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Pull-down weerstand

# --- Pygame Setup voor 2 HDMI-schermen ---
pygame.init()
screen1 = pygame.display.set_mode((640, 480), pygame.NOFRAME, display=0)  # Auto 1
screen2 = pygame.display.set_mode((640, 480), pygame.NOFRAME, display=1)  # Auto 2
font = pygame.font.Font(None, 50)

# --- Functies ---
def buzzer_on():
    GPIO.output(buzzer_pin, GPIO.HIGH)

def buzzer_off():
    GPIO.output(buzzer_pin, GPIO.LOW)

def clear_leds():
    pixels.fill((0, 0, 0))
    pixels.show()

def start_lights():
    """Startprocedure met LED's en buzzer"""
    for i in range(LED_COUNT):
        pixels[i] = (255, 0, 0)
        pixels.show()
        buzzer_on()
        time.sleep(0.2)
        buzzer_off()
        time.sleep(0.3)

    time.sleep(3)  # Wachten voor start
    clear_leds()
    
    buzzer_on()
    time.sleep(1)  # Startsituatie
    buzzer_off()

def update_screen(screen, car_number):
    """Scherm updaten met laatste rondetijd"""
    screen.fill((0, 0, 0))  
    if car_times[car_number]:
        text = font.render(f"Auto {car_number} - Laatste Tijd: {car_times[car_number][-1]:.3f} sec", True, (255, 255, 255))
    else:
        text = font.render(f"Auto {car_number} - Wachten...", True, (255, 255, 255))
    
    screen.blit(text, (50, 200))
    pygame.display.flip()

def scan_rfid():
    """RFID uitlezen en rondetijden bijhouden"""
    print("Wacht op RFID...")
    while True:
        id, text = reader.read()
        timestamp = time.time()

        # Pas ID's aan voor je eigen RFID-tags!
        car_number = 1 if id == 123456789 else 2  

        if last_lap[car_number]:
            lap_time = round(timestamp - last_lap[car_number], 3)
            car_times[car_number].append(lap_time)
            print(f"Auto {car_number}: {lap_time} sec")

        last_lap[car_number] = timestamp

        # Juiste scherm bijwerken
        if car_number == 1:
            update_screen(screen1, 1)
        else:
            update_screen(screen2, 2)

        time.sleep(0.5)

def reset_system():
    """Reset de timing en schermen"""
    print("Reset ingedrukt! Timing wordt gereset.")
    global car_times, last_lap
    car_times = {1: [], 2: []}
    last_lap = {1: 0, 2: 0}
    clear_leds()  # Zet de LED's uit
    pygame.display.quit()  # Sluit de oude schermen af
    pygame.init()  # Herinitialiseer Pygame
    # Maak nieuwe schermen aan
    screen1 = pygame.display.set_mode((640, 480), pygame.NOFRAME, display=0)  # Auto 1
    screen2 = pygame.display.set_mode((640, 480), pygame.NOFRAME, display=1)  # Auto 2
    time.sleep(1)  # Wacht kort om alles te resetten

# --- Hoofdprogramma ---
try:
    print("Druk op de startknop om de race te beginnen...")

    # Wachten tot de startknop wordt ingedrukt
    while GPIO.input(start_button) == GPIO.LOW:
        time.sleep(0.1)

    print("Startknop ingedrukt! Startprocedure begint...")
    start_lights()  # F1 startlichtsequentie
    
    while True:
        # Als de resetknop ingedrukt wordt, reset alles
        if GPIO.input(reset_button) == GPIO.HIGH:
            reset_system()  # Reset het systeem

        scan_rfid()  # RFID timing starten

except KeyboardInterrupt:
    print("\nAfsluiten...")
    clear_leds()
    GPIO.cleanup()
```

---

### Uitleg van de Code:
- **F1 Startlicht en Buzzer**: De `start_lights()` functie simuleert de F1 startprocedure, waarbij LED's en buzzer samen werken. Na de startlicht sequentie, klinkt er een geluid voor 1 seconde om het begin van de race aan te geven.
- **RFID Timing**: De `scan_rfid()` functie registreert de tijden van de auto's op basis van hun RFID-tag. De tijden worden opgeslagen en weergegeven op twee verschillende schermen.
- **Resetknop**: De resetknop zorgt ervoor dat de tijden en schermen worden gewist en alles opnieuw begint.
- **Twee schermen via HDMI**: De `pygame` bibliotheek wordt gebruikt om twee aparte schermen aan te sturen met verschillende timing-informatie voor elke auto.

### Stap 3: Uitvoering
1. **Verbind alles volgens de bovenstaande aansluitingen**.
2. **Start het script** met:
   ```bash
   python3 f1_start_rfid.py
   ```
3. **Druk op de startknop** om de race te starten.
4. **Druk op de resetknop** om de timing en schermen te resetten.

---

Als je alles hebt aangesloten en het script draait, kun je de race starten en de tijden volgen voor beide auto's op twee verschillende schermen! 
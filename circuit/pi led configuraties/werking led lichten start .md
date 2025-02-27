# Benodigheden:
1. **LED's knipperen** na het uitgaan (5 seconden).
2. **Buzzer** die geluid maakt tijdens het aftellen.
3. **Startsignaal** voor 2 seconden aan het eind.

### Benodigdheden:
- **Buzzer** (bijvoorbeeld een actieve piezo buzzer).
- **LED's** (
- **Weerstand voor de buzzer** (meestal niet nodig voor actieve buzzers).
- **Extra GPIO-pin** voor de buzzer (bijv. GPIO 13).

### Stappen:

#### 1. **Sluit de buzzer aan**
Sluit de buzzer aan op een vrije GPIO-pin, bijvoorbeeld GPIO13. Verbind de positieve kant van de buzzer naar de GPIO en de negatieve kant naar de GND van de Raspberry Pi.

#### 2. **Pas de code aan**
Hier is de aangepaste code die de buzzer laat aftellen samen met de LED's en daarna het startsignaal geeft:

```python
import RPi.GPIO as GPIO
import time

# Zet de GPIO mode in
GPIO.setmode(GPIO.BCM)

# Definieer de GPIO-pinnen voor de vijf LED's en de buzzer
led_pins = [17, 27, 22, 5, 6]
buzzer_pin = 13  # Buzzer aangesloten op GPIO13

# Zet de GPIO-pinnen als uitvoer
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Functie om de buzzer aan en uit te zetten
def buzzer_on():
    GPIO.output(buzzer_pin, GPIO.HIGH)  # Zet buzzer aan

def buzzer_off():
    GPIO.output(buzzer_pin, GPIO.LOW)   # Zet buzzer uit

# Functie voor het knipperen van de LED's
def leds_blinking():
    for i in range(5):
        for pin in led_pins:
            GPIO.output(pin, GPIO.HIGH)  # Zet LED aan
        buzzer_on()
        time.sleep(0.2)  # Wacht 0.2 seconden
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)  # Zet LED uit
        buzzer_off()
        time.sleep(0.2)  # Wacht 0.2 seconden

# Functie voor het startsignaal
def start_signal():
    for i in range(5):  # Startsignaal met 5 seconden knipperen
        for pin in led_pins:
            GPIO.output(pin, GPIO.HIGH)  # Zet LED aan
        buzzer_on()
        time.sleep(0.2)  # Wacht 0.2 seconden
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)  # Zet LED uit
        buzzer_off()
        time.sleep(0.2)  # Wacht 0.2 seconden
    time.sleep(2)  # Na het knipperen 2 seconden wachten voor het startsignaal

try:
    # Zet de LED's één voor één aan
    for i in range(len(led_pins)):
        GPIO.output(led_pins[i], GPIO.HIGH)  # Zet LED aan
        time.sleep(0.5)  # Wacht 0.5 seconde tussen het aansteken van elke LED
    
    # Wacht 2 seconden nadat alle LED's aan zijn
    time.sleep(2)

    # Zet alle LED's uit
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)
    
    # Laat de LED's knipperen voor 5 seconden en de buzzer klinkt samen
    leds_blinking()

    # Geef het startsignaal voor 2 seconden
    start_signal()

except KeyboardInterrupt:
    pass

finally:
    # Zet alle pinnen terug naar inputstatus om GPIO schoon te maken
    GPIO.cleanup()
```

### Wat doet de code?
1. **LED's één voor één aanzetten**: Zoals in je oorspronkelijke vraag.
2. **Na het uitgaan van de LED's**:
   - De LED's beginnen 5 seconden lang te knipperen, waarbij de buzzer elke keer mee piept (knippert samen met de LED's).
3. **Startsignaal**:
   - Na de knipperperiode van 5 seconden worden de LED's opnieuw 5 keer aangestoken met de buzzer die ook mee piept. Dit is je startsignaal, dat 2 seconden duurt.

### Uitleg van de nieuwe functies:
- **`buzzer_on()` en `buzzer_off()`**: Functies om de buzzer aan en uit te zetten.
- **`leds_blinking()`**: Laat de LED's knipperen gedurende 5 seconden, samen met de buzzer die geluid maakt.
- **`start_signal()`**: Start de LED's en buzzer voor 5 keer knipperen en wacht dan 2 seconden voor een startsignaal.

### Testen:
sluit alles aan en voer het script uit:

```bash
python3 leds_buzzer.py
```
---

---

## 🔧 **Benodigdheden**
1. **Raspberry Pi** (bijv. Raspberry Pi 4 of Zero W)  
2. **WS2812B LED-strip (Neopixel)** (minstens 5 LED’s)  
3. **Buzzer** (actieve piezo-buzzer, 5V)  
4. **Voeding voor LED-strip** (bijv. 5V 2A adapter)  
5. **330Ω weerstand** (tussen Pi en DIN van LED-strip, voorkomt signaalproblemen)  
6. **Jumper wires**  

---

## 🔌 **Stap 1: Aansluiten van de hardware**
| LED-strip | Raspberry Pi |
|-----------|--------------|
| **DIN (Data In)** | **GPIO 18 (PWM)** |
| **5V** | **5V (indien <10 LED’s)** |
| **GND** | **GND (deel met buzzer & Pi)** |

| Buzzer | Raspberry Pi |
|--------|--------------|
| **+ (Positief)** | **GPIO 13** |
| **- (Negatief)** | **GND** |

⚠️ **LET OP:**  
- Gebruik **een aparte 5V-voeding** voor de LED-strip als je **meer dan 10 LED’s** hebt.  
- **GND’s van de voeding en de Raspberry Pi moeten verbonden zijn!**  

---

## 💾 **Stap 2: Software installeren**
1. Open een terminal op de Raspberry Pi en installeer de WS2812B-bibliotheek:
   ```bash
   sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
   ```

2. Schakel de audio-uitgang uit (deze gebruikt dezelfde PWM-pin als de LED-strip):
   ```bash
   sudo nano /boot/config.txt
   ```
   Voeg deze regel toe (of wijzig als die er al staat):
   ```
   dtparam=audio=off
   ```
   Sla op (Ctrl + X → Y → Enter) en herstart:
   ```bash
   sudo reboot
   ```

---

## 🖥 **Stap 3: Code voor startlichten**
Hier is de volledige code. Kopieer en plak deze in een nieuw Python-bestand:  

```python
import time
import board
import neopixel
import RPi.GPIO as GPIO

# Configuratie
LED_COUNT = 5  # Aantal rode lichten
LED_PIN = board.D18  # GPIO 18 (PWM)
BRIGHTNESS = 0.5  # Helderheid (0.0 - 1.0)
buzzer_pin = 13  # Buzzer op GPIO 13

# LED-strip initialiseren
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=BRIGHTNESS, auto_write=False)

# Buzzer instellen
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Functies voor de buzzer
def buzzer_on():
    GPIO.output(buzzer_pin, GPIO.HIGH)

def buzzer_off():
    GPIO.output(buzzer_pin, GPIO.LOW)

# Zet alle LED's uit
def clear_leds():
    pixels.fill((0, 0, 0))
    pixels.show()

# Startsequentie: LED's één voor één rood laten oplichten met buzzer
def start_lights():
    for i in range(LED_COUNT):
        pixels[i] = (255, 0, 0)  # Rood
        pixels.show()
        buzzer_on()
        time.sleep(0.2)  # Korte piep
        buzzer_off()
        time.sleep(0.3)  # Totaal 0.5 sec per LED
    
    time.sleep(3)  # 3 seconden alle LED's aan

    clear_leds()  # LED's uit

    # Startsignaal (buzzer 1 sec aan)
    buzzer_on()
    time.sleep(1)
    buzzer_off()

try:
    start_lights()

except KeyboardInterrupt:
    clear_leds()
    GPIO.cleanup()
finally:
    clear_leds()
    GPIO.cleanup()
```

---

## ▶️ **Stap 4: Programma uitvoeren**
1. Sla de code op als `startlichten.py`:
   ```bash
   nano startlichten.py
   ```
   **Plak de code en sla op** (Ctrl + X → Y → Enter).  

2. Voer het programma uit:
   ```bash
   python3 startlichten.py
   ```

---

## 🚦 **Wat gebeurt er?**
1. **LED's gaan één voor één rood aan** (0.5 sec per LED) met een **korte buzzerpiep per LED**.  
2. **Na 3 seconden gaan alle LED's uit**.  
3. **De buzzer klinkt 1 seconde als startsignaal**.  
4. **Einde**.  

---

## 🛠 **Mogelijke uitbreidingen**
🔹 **Meer LED’s?** Pas `LED_COUNT = X` aan.  
🔹 **Andere kleuren?** Verander `(255, 0, 0)` naar bijvoorbeeld `(0, 0, 255)` voor blauw.  
🔹 **Andere timing?** Pas de `time.sleep()` waarden aan.  

---

# nu met rfid geintegreerd

We gaan het **F1-startlichtsysteem**, **RFID-timing** en **twee HDMI-schermen** combineren in één geïntegreerde code.  

---

## 🚦 **Wat gaat het script doen?**  
1. **Startprocedure**:  
   - LED’s gaan één voor één rood aan.  
   - Buzzer piept bij elke LED.  
   - Na 3 seconden gaan alle LED’s uit en de buzzer geeft een startsignaal.  

2. **Live Rondetiming per auto**:  
   - **Scherm 1:** Rondetijden van **Auto 1**  
   - **Scherm 2:** Rondetijden van **Auto 2**  

---

## 🔧 **Benodigdheden**  
1. **Raspberry Pi 4** met **twee HDMI-schermen**.  
2. **Adreseerbare WS2812B LED’s** (op GPIO 18).  
3. **Actieve buzzer** (op GPIO 13).  
4. **RFID-lezer (MFRC522 of PN532)** (SPI op de Pi aanzetten!).  
5. **Twee RFID-tags (één per auto)**.  

---

## 🖥 **Code: F1-start + RFID-timing op 2 schermen**
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

# --- Hoofdprogramma ---
try:
    start_lights()  # F1 startlichtsequentie
    scan_rfid()  # RFID timing starten

except KeyboardInterrupt:
    print("\nAfsluiten...")
    clear_leds()
    GPIO.cleanup()
```

---

## 🚀 **Wat gebeurt er?**
1. **Startprocedure**  
   - LED’s gaan **één voor één aan**.  
   - Buzzer piept bij elke LED.  
   - Na 3 sec gaan LED’s uit en buzzer geeft een **startsignaal**.  

2. **Live Rondetiming**  
   - **Scherm 1:** Auto 1 rondetijden  
   - **Scherm 2:** Auto 2 rondetijden  

---

## 🔥 **Hoe te starten?**
1. **Sluit alles aan** (RFID, LED's, buzzer, HDMI-schermen).  
2. **Start het script** met:  
   ```bash
   python3 f1_start_rfid.py
   ```
3. **Plaats een RFID-tag op de lezer** → Scherm toont rondetijd!  

---

### ✅ **Extra mogelijkheden**  
- **Laptijden opslaan naar CSV** voor analyse?  
- **Schermen een race-timer laten tonen**?  
- **Meerdere auto’s toevoegen** (tot 4 schermen met extra Pi’s!)?  










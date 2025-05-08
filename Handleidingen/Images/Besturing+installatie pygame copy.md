# Auto

Verbinden van een stuur en pedalen met een Raspberry Pi en het signaal uitlezen.
![logitech stuur + pedalen](/Besturing/Images/image.png)

We zullen het stuur en de pedalen met een usb verbinden aan de raspberry pi (want er zit een usb verbinding op rapsberry pi).
![Raspberry Pi](/Besturing//Images/image-1.png)
Om de ingangen van het stuur en pedalen uit te lezen hebben we een softwarebibliotheek nodig die de HID-apparaten ondersteunt voor op onze raspberry pi te kunnen programmeren.
•evdev (voor Linux HID-apparaten) eenvoudig en makkelijke implementatie
•pygame (heeft joystick-ondersteuning)
•hidapi (voor direct uitlezen van HID-apparaten) snelheid en efficiënt.

Wij kunnen gebruik maken van evdev en hidapi voor het uitlezen van de HID-apparaten. De pygame kunnen we ook wel gebruiken maar de joystick ondersteuning hebben we niet nodig.
We zullen de waarden van het stuur of de hoek dat we hebben moeten omzetten naar een PWM-signaal, want het zijn binaire waarden of signalen die we binnenkrijgen van het stuur en de pedalen.

Word verbonden met een antenne van de auto zelf (microcontroller).
![ESP32](/Besturing/Images/image-2.png)

## Pygame (programma voor Rp4)

Pygame zorgt ervoor dat je eenvoudig de stuurhoek, pedalen en knoppen kunt uitlezen zonder gedoe met ruwe HID-data.

*Stap 1:* Pygame installeren op Raspberry Pi

```bash
pip install pygame
```

Controleer daarna of het goed werkt met:

```python
python3 -c "import pygame; print(pygame.ver)"
```

*Stap 2:* Controller herkennen en verbinden

Je kunt eerst checken hoeveel joysticks/stuuren er zijn aangesloten:

```python
import pygame

pygame.init()

joystick_count = pygame.joystick.get_count()
print(f"Aantal joysticks gevonden: {joystick_count}")

for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    print(f"Joystick {i}: {joystick.get_name()}")

```

Als het stuur correct wordt herkend, zie je zoiets als:
(de volgende code is yaml)

```python
Aantal joysticks gevonden: 1
Joystick 0: Logitech G29 Driving Force Racing Wheel
```

*Stap 3:* Stuur en pedalen uitlezen

Gebruik deze code om de stuurhoek, gas, rem en koppeling live te lezen:

```python
import pygame

pygame.init()

# Stuur verbinden
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Stuur gevonden: {joystick.get_name()}")

# Haal aantal assen en knoppen op
axes = joystick.get_numaxes()
buttons = joystick.get_numbuttons()

print(f"Aantal assen: {axes}, Aantal knoppen: {buttons}")

try:
    while True:
        pygame.event.pump()  # Evenementen updaten
        
        # Stuurpositie (-1 = volledig links, 1 = volledig rechts)
        steering = joystick.get_axis(0)

        # Pedalen (0 = losgelaten, 1 = volledig ingedrukt)
        throttle = (joystick.get_axis(2) + 1) / 2  # Gas
        brake = (joystick.get_axis(3) + 1) / 2  # Rem
        clutch = (joystick.get_axis(1) + 1) / 2  # Koppeling (als beschikbaar)

        # Knoppen uitlezen (bijv. knop 0 = X op G29)
        button_states = [joystick.get_button(i) for i in range(buttons)]

        print(f"Stuur: {steering:.2f}, Gas: {throttle:.2f}, Rem: {brake:.2f}, Koppeling: {clutch:.2f}, Knoppen: {button_states}")

except KeyboardInterrupt:
    print("\nAfsluiten...")
    pygame.quit()
```

Hoe de data werkt

get_axis(0) → Stuurpositie (-1.0 tot 1.0)

get_axis(2) → Gas (-1.0 tot 1.0) → Omzetten naar 0-1 met +1 / 2

get_axis(3) → Rem (-1.0 tot 1.0) → Ook omzetten naar 0-1

get_axis(1) → Koppeling (-1.0 tot 1.0, alleen op G29)

get_button(n) → Knopstatus (1 als ingedrukt, anders 0)

## Pygame is met een extra bib genaamd SDL2

SDL2 (Simple DirectMedia Layer 2) is een krachtige multimedia-bibliotheek die Pygame onder de motorkap gebruikt voor het werken met:

🎮 Joysticks & stuurwielen

🎧 Audio

🖥 Grafische weergave & vensters

⌨️ Toetsenbordinvoer

Pygame is eigenlijk een wrapper om SDL2 heen, wat betekent dat Pygame intern SDL2 gebruikt om toegang te krijgen tot hardware zoals je Logitech stuur en pedalen.

🔍 Waarom is SDL2 belangrijk voor je stuur en pedalen?

+ SDL2 zorgt ervoor dat Pygame automatisch je stuur herkent.

+ Het maakt stuurassistentie, deadzones en force feedback makkelijker.

+ Het is cross-platform, dus het werkt op Windows, Linux (Raspberry Pi), en macOS.

+ SDL2 ondersteunt direct joysticks/gamepads/racesturen zonder dat je zelf HID-rapporten hoeft te decoderen.

We zullen een stuk code schrijven zodat we het stuur en pedalen kunnen binnenlezen en da ook kunnen uitlezen.

We zullen nu de code **per sectie** uitleggen.

📜 Code uitleg per sectie

## 1. Importeren van de benodigde libraries

```python
import pygame
import time
import RPi.GPIO as GPIO  # Voor PWM-output
```

+ pygame wordt gebruikt om input van het Logitech G923 stuur en pedalen uit te lezen.

+ time zorgt ervoor dat we een kleine pauze in de loop kunnen zetten om CPU-overbelasting te voorkomen.

+ RPi.GPIO wordt gebruikt om PWM-signalen naar de Traxxas-zender te sturen via de GPIO-pinnen van de Raspberry Pi.

## 2. GPIO-instellingen voor PWM-output

```python
# GPIO-pinnen voor PWM
PWM_PIN_STEERING = 18  # GPIO voor stuur
PWM_PIN_THROTTLE = 19  # GPIO voor gas/rem

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN_STEERING, GPIO.OUT)
GPIO.setup(PWM_PIN_THROTTLE, GPIO.OUT)

# PWM-initialisatie (50Hz, geschikt voor servo-aansturing)
steering_pwm = GPIO.PWM(PWM_PIN_STEERING, 50)
throttle_pwm = GPIO.PWM(PWM_PIN_THROTTLE, 50)
steering_pwm.start(7.5)  # Neutrale positie
throttle_pwm.start(7.5)
```

Wat gebeurt hier?

✅ GPIO18 wordt gebruikt voor het sturen (PWM-signaal naar de Traxxas-zender).

✅ GPIO19 wordt gebruikt voor gas/rem (ook een PWM-signaal).
✅ GPIO.setmode(GPIO.BCM) zorgt ervoor dat we de BCM-nummers van de Raspberry Pi gebruiken.

✅ GPIO.setup() stelt de pinnen in als output.

✅ PWM wordt gestart op 50Hz, wat een standaard servo-frequentie is.
✅ Startwaarden worden op 7.5% duty cycle gezet, wat overeenkomt met de neutrale stand van een servo.

## 3. pygame initialiseren voor het Logitech G923 stuur

```python
# pygame init
pygame.init()
pygame.joystick.init()

# Zoek en initialiseer het stuur
joystick = pygame.joystick.Joystick(0)
joystick.init()
```

Wat gebeurt hier?

✅ pygame.init() start pygame.

✅ pygame.joystick.init() zet de joystick-module van pygame aan.

✅ joystick = pygame.joystick.Joystick(0) zoekt de eerste aangesloten joystick (Logitech G923).

✅ joystick.init() initialiseert het stuur zodat we data kunnen uitlezen.

## 4. Functies om waarden om te zetten naar PWM

```python
def scale(value, src_range, dst_range):
    """Schaal een waarde van een bronbereik naar een doelbereik."""
    (src_min, src_max), (dst_min, dst_max) = src_range, dst_range
    return dst_min + (float(value - src_min) / float(src_max - src_min)) * (dst_max - dst_min)
```

Wat doet deze functie?

Deze schaalt een inputwaarde naar een ander bereik.
Bijvoorbeeld: het stuur levert een waarde tussen -1 (links) en 1 (rechts), maar PWM moet een duty cycle tussen 5% en 10% krijgen.
De functie rekent automatisch om naar het juiste bereik.

Initialisatie van de variabelen:

```python
reverse_throttle = False # Variable om de richting van het gas bij te houden
pwm_value = scale(-1, (-1, 1), (5, 10))  # -1 wordt omgezet naar 5% duty cycle
pwm_value = scale(1, (-1, 1), (5, 10))   # 1 wordt omgezet naar 10% duty cycle
print(f"Steering PWM Value: {pwm_value_steering}")
print(f"Throttle PWM Value: {pwm_value_throttle}")

```

Nu maken we nog een functie aan voor de duty_cycle

```python
def set_pwm(pwm, value):
    """Stuur een PWM-signaal (bijv. naar een servo) en retourneer de duty cycle"""
    duty_cycle = scale(value, (-1, 1), (5, 10))  # Standaard servo PWM-bereik
    pwm.ChangeDutyCycle(duty_cycle)
    return duty_cycle  # Geeft de berekende duty cycle terug
```

Wat doet deze functie?

+ Neemt een stuur- of gaspedaalwaarde tussen -1 en 1.
+ Schaalt deze om naar PWM tussen 5% (min) en 10% (max).
+ Stuurt deze waarde naar de Raspberry Pi PWM-output.

## 5. De hoofdloop om alles te laten werken

```python
try:
    print("G923-besturing actief...")

    while True:
        pygame.event.pump()

        # Stuur (-1 = links, 1 = rechts)
        steering = joystick.get_axis(0)
        print(f"Stuur: {steering:.2f}")

        # Gas (-1 = geen gas, 1 = vol gas)
        throttle = joystick.get_axis(2)
        print(f"Gas: {throttle:.2f}")

        # Rem (-1 = geen rem, 1 = volle rem)
        brake = joystick.get_axis(3)
        print(f"Rem: {brake:.2f}")

        #Controleer of de rechter shiftknop is ingedrukt
        if joystick.get_button(4):
            reverse_throttle = not reverse_throttle # Wissel de richting om
            # Toon de nieuwe status in de shell
            if reverse_throttle:
                print("Richting: Achteruit")
            else:
                print("Richting: Vooruit")
            time.sleep(0.3)

        # Bereken throttle output (gas en rem samenvoegen)
        if throttle > -0.9:  # Gas ingedrukt
            throttle_output = throttle if not reverse_throttle else -throttle #Als reverse_throttle waar is, omgekeerd gas
        elif brake > -0.9:  # Rem ingedrukt
            throttle_output = -brake
        else:
            throttle_output = 0  # Neutraal

        # Stuur PWM naar de Traxxas-zender
        set_pwm(steering_pwm, steering)  # Stuurhoek
        set_pwm(throttle_pwm, throttle_output)  # Gas/rem

        time.sleep(0.05)  # Voorkom CPU-overbelasting
```

Wat gebeurt hier?

✅ while True: zorgt ervoor dat de code blijft draaien.

✅ pygame.event.pump() verwerkt de joystick-events.

✅ joystick.get_axis(0) leest de stuurinput (-1 = links, 1 = rechts).

✅ joystick.get_axis(2) leest het gas (-1 = geen gas, 1 = vol gas).

✅ joystick.get_axis(3) leest de rem (-1 = geen rem, 1 = volle rem).

✅ Throttle-output wordt berekend door gas en rem samen te voegen.

✅ De waarden worden omgezet naar PWM en naar de GPIO-uitgangen gestuurd.

✅ time.sleep(0.05) voorkomt dat de CPU te hard belast wordt.

## 6. Netjes afsluiten bij een toetsenbordonderbreking

```python
except KeyboardInterrupt:
    print("\nAfsluiten...")
    steering_pwm.stop()
    throttle_pwm.stop()
```

Wat gebeurt hier?

+ Als je CTRL+C indrukt, stopt het script netjes.
+ PWM-signalen worden gestopt (.stop()).
+ GPIO wordt opgeschoond (GPIO.cleanup()), zodat andere programma’s geen problemen krijgen.
+ pygame wordt afgesloten (pygame.quit()).

## 🎯 Samenvatting

✅ Leest Logitech G923 stuur & pedalen uit met pygame.

✅ Schaalt de stuurinvoer (-1 tot 1) om naar PWM (5% - 10%).

✅ Stuurt PWM-signalen uit via GPIO18 (stuur) en GPIO19 (gas/rem).

✅ Werkt zonder DAC, dus direct op de Raspberry Pi GPIO.

✅ Veilig afsluiten bij CTRL+C.

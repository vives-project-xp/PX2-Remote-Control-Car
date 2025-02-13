# Auto

Verbinden van een stuur en pedalen met een Raspberry Pi en het signaal uitlezen.
![logitech stuur + pedalen](image.png)

We zullen het stuur en de pedalen met een usb verbinden aan de raspberry pi (want er zit een usb verbinding op rapsberry pi).
![Raspberry Pi](image-1.png)
Om de ingangen van het stuur en pedalen uit te lezen hebben we een softwarebibliotheek nodig die de HID-apparaten ondersteunt voor op onze raspberry pi te kunnen programmeren.
•	evdev (voor Linux HID-apparaten) eenvoudig en makkelijke implementatie
•	pygame (heeft joystick-ondersteuning)
•	hidapi (voor direct uitlezen van HID-apparaten) snelheid en efficiënt.


Wij kunnen gebruik maken van evdev en hidapi voor het uitlezen van de HID-apparaten. De pygame kunnen we ook wel gebruiken maar de joystick ondersteuning hebben we niet nodig.
We zullen de waarden van het stuur of de hoek dat we hebben moeten omzetten naar een PWM-signaal, want het zijn binaire waarden of signalen die we binnenkrijgen van het stuur en de pedalen.

Word verbonden met een antenne van de auto zelf (microcontroller).
![ESP32](image-2.png)


**Pygame (programma voor Rp4)**

Pygame zorgt ervoor dat je eenvoudig de stuurhoek, pedalen en knoppen kunt uitlezen zonder gedoe met ruwe HID-data.

*Stap 1:* Pygame installeren op Raspberry Pi

```
pip install pygame
```
Controleer daarna of het goed werkt met:

```
python3 -c "import pygame; print(pygame.ver)"
```
*Stap 2:* Controller herkennen en verbinden

Je kunt eerst checken hoeveel joysticks/stuuren er zijn aangesloten:

```
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
```
Aantal joysticks gevonden: 1
Joystick 0: Logitech G29 Driving Force Racing Wheel

```

*Stap 3:* Stuur en pedalen uitlezen

Gebruik deze code om de stuurhoek, gas, rem en koppeling live te lezen:
```
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

**Pygame is met een extra bib genaamd SDL2**

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


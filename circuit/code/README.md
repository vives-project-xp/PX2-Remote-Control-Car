# Dashboard en lichten code

## Contents

In deze folder bevindt zich de code voor het dashboard en de lichten aan te sturen. Dit zijn de 2 bestanden [Dashboard_lights.py](Dashboard_lights.py) en [light_control.py](./light_control.py).
Verder zitten ook de geluidsbestanden [long_beep.wav](./long_beep.wav) en [smal_Beep.wav](smal_Beep.wav) in deze folder.

## Hoe gebruiken

Voor het programma te laten draaien moet je alleen Dashboard_lights.py runnen, hiermee zullen lichten, geluid en dashboard werken.
Beide bestanden moeten wel in dezelfde folder staan op een raspi 4 samen met de 2 geluidsbestanden.

## Dependencies

Om de code te gebruiken moet je een aantal python libraries installeren op de pi. Deze bevinden zich in requirements.txt.
Voor de dependencies snel te installeren kan je volgend command gebruiken in de terminal.

```bash
pip install -r requirements.txt
```

## Uitleg code

### light_control.py

In dit bestand wordt de class LightControl gemaakt. Deze wordt dan in Dashboard_lights.py gebruikt voor de lichten aan te sturen.
De class heeft een aantal functies die nodig zijn voor alles te laten werken.

#### start_sequence

Deze methode start de sequentie van de lichten, ze gaan 1 voor 1 aan met een geluidje (small_beep) op de achtergrond. Achter dat ze alle 5 aan zijn zullen de lichten achter een willekeurige tijd van 1,2 tot 1,8 seconde uit gaan en zal er een ander geluidje (long_beep) afgaan.

```python
def start_sequence(self):
        # verdeel ledstrip in 5 stukken die licht geven
        segments = [(5, 10), (22, 28), (42, 48), (62, 68), (80, 85)]
        
        # Initial reset
        self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()
        # methode die reset doet achter 1 seconde
        if self._wait_with_reset(1):
            return

        # Segment activation
        for start, end in segments:
            self.pixels[start:end] = [(255, 0, 0, 0)] * (end - start)
            self.pixels.show()
            self.small_beep.play()
            # methode die reset doet achter 1 seconde
            if self._wait_with_reset(1):
                return

        # Final sequence
        if self._wait_with_reset(1 + random.uniform(0.2, 0.8)):
            return
        self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()
        self.long_beep.play()
        # methode die reset doet achter geluid stopt
        self._play_long_beep_with_reset()
```

#### reset_lights

Deze methode reset alle lichten naar hun originele status en stopt het geluid.

```python
    def reset_lights(self):
        # zet de kleur naar 0
        self.pixels.fill((0, 0, 0, 0))
        # toont de lichten, deze zijn normaal uit
        self.pixels.show()
        # Zet het geluid uit
        pygame.mixer.stop()
        # update de drukknoppen
        self._update_button_leds()
```

### Dashboard_lights.py

In dit codebestand wordt de RFID ingeleven en wordt ook het dashboard aangemaakt en bijgestuurd.

#### initializeer variabelen

```python
start_ticks = 0  # Houdt de starttijd bij wanneer de timer begint
time_str = "00:00.000"  #verstreken tijd in minuten, seconden en milliseconden
auto1_name = "Oranje auto"  # Naam van auto 1(Oranje auto)
auto2_name = "Rode auto"  # Naam van auto 2(Rode auto)
auto1_time = "00:00.000"  # Verstreken tijd voor auto 1
auto2_time = "00:00.000"  # Verstreken tijd voor auto  2
auto1_stopped = False  # Boolean die aangeeft of auto 1 is gestopt
auto2_stopped = False  # Boolean die aangeeft of auto 2 is gestopt
auto1_stop_ticks = 0  # Houdt de tijd bij waarop auto 1 is gestopt
auto2_stop_ticks = 0  # Houdt de tijd bij waarop auto 2 is gestopt
timer_stopped = 0  # Boolean die aangeeft of de timer is gestopt
timer_running = False  # Boolean die aangeeft of de timer momenteel loopt
```

#### parse_tag_id

Deze functie zet de ontvangen data van de RFID lezer om naar een tag ID moest deze aanwezig zijn. Deze wordt dan verder in de code gebruikt om te vergelijken met een target tag waar elke auto 1 van heeft. De tag is verschillend per auto om ze zo van elkaar te onderscheiden.

```python
def parse_tag_id(data):
    # kijken of data lang genoeg is en als de header klopt.
    if len(data) < 6 or data[0] != 0xBB or data[2] != 0x22:
        return None
    
    # Data lengte
    data_length = data[3]
    
    # kijken of paket compleet is
    if len(data) < 5 + data_length + 2:
        return None
    
    # begin en einde van tag ID vinden
    tag_start = 6
    tag_end = tag_start + 12
    if tag_end > len(data) - 2:
        return None
    
    # tag ID in bytes
    tag_bytes = data[tag_start:tag_end]
    
    # omzetten naar ID in hexadecimale notatie
    return tag_bytes.hex().upper()
```

De rest van de code wordt uitgelegd in de codebestanden zelf in comments
[light_control.py](light_control.py)
[Dashboard_lights.py](Dashboard_lights.py)

# Dashboard en lichten code

## Hoe gebruiken

Voor lichten en dashboard hebben we 2 code bestanden Dashboard_lights.py en light_control.py. Voor het programma te laten draaien moet je alleen Dashboard_lights.py runnen, hiermee zullen lichten en dashboard werken.

## Uitleg code

### light_control.py

In dit bestand wordt de class LightControl gemaakt. Deze wordt dan in Dashboard_lights.py gebruikt voor de lichten aan te sturen. De class heeft een aantal functies die nodig zijn voor alles te laten werken.

#### start_sequence

Deze functie start de sequentie van de lichten, ze gaan 1 voor 1 aan met een geluidje (small_beep) op de achtergrond. Achter dat ze alle 5 aan zijn zullen de lichten achter een willekeurige tijd van 1,2 tot 1,8 seconde uit gaan en zal er een ander geluidje (long_beep) afgaan.

```python
def start_sequence(self):
        
        segments = [(5, 10), (22, 28), (42, 48), (62, 68), (80, 85)]
        
        # Initial reset
        self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()
        if self._wait_with_reset(1):
            return

        # Segment activation
        for start, end in segments:
            self.pixels[start:end] = [(255, 0, 0, 0)] * (end - start)
            self.pixels.show()
            self.small_beep.play()
            if self._wait_with_reset(1):
                return

        # Final sequence
        if self._wait_with_reset(1 + random.uniform(0.2, 0.8)):
            return
        
        self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()
        self.long_beep.play()
        self._play_long_beep_with_reset()
```
#### reset_lights

Deze functie reset alle lichten naar hun originele status en stopt het geluid.

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

# Auto Besturing met een Raspberry Pi

## Stap 1: Verwijder de PCB van de controller

We merken dat de besturing van de auto gebeurt door aan potentiometers te draaien. Hierdoor kunnen wij nu een spanning in de plaats van die potentiometers steken om zo de auto aan te sturen.

### Test
We kunnen de aansluiting testen door de potentiometers te vervangen door een spanningsbron en te observeren wat er gebeurt:
- Links = **0V**
- Rechts = **3,3V**
- Neutraal = **1,65V**
- **Gas geven**: 0V = volle gas vooruit
- **Achteruit**: 3,3V = volle snelheid achteruit

## Stap 2: Verbinden met een Raspberry Pi

Een Raspberry Pi kan niet zomaar een spanning uitsturen. Gelukkig is er een oplossing: **PWM (Pulse Width Modulation)**.

1. We bekijken welke pinnen **PWM-pinnen** zijn op onze Raspberry Pi.
2. We merken dat de PWM-signalen zeer wisselvallig zijn, waardoor pieken en dalen in spanning verschijnen. Dit kan ervoor zorgen dat de auto plots in gang schiet.
3. Oplossing: **Low-pass filter** gebruiken om de signalen uit te vlakken.
   - **Componenten**:
     - **1kΩ weerstand** in serie
     - **22pF condensator** naar de grond

## Stap 3: Een programma schrijven

Het programma moet de inputs lezen en omzetten naar een spanningsoutput. Dit kan bijvoorbeeld met Python en de `RPi.GPIO` of `pigpio` bibliotheek.

```
```

Dit programma laat je de PWM duty cycle aanpassen, waardoor de auto gestuurd kan worden met de juiste spanning.

---

Met deze stappen kunnen we de auto correct besturen via een Raspberry Pi!

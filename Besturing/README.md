# Documentatie van Besturing

Hierin staat alle nodige info over de besturing.

## Inhoudstafel

- [Images](./Images/): Hier bevinden zich foto's over besturing en PCB
- [MCU van de RC-controller](./MCU%20van%20de%20RC-controller/): Hier bevindt zich de datasheet van MCU en RC controller
- [PCB](./PCB/): Hier bevinden zich de bestanden van de PCB.
- [Autostart](./Autostart.md):
- [BesturingCompleet](./BesturingCompleet.md): In dit bestand word de besturing uitgelegd
- [Code Raspberry Pi](./Code%20Raspberry%20Pi.py): Dit is code voor besturing auto zonder exponentiele versnelling.
- [Eind versie besturing-car](./eind%20versie%20besturing-car): Dit is laatste versie van code voor besturing.
- [Requirements](./requirements.txt): Dit bestand bevat de dependencies voor code controller.
- [Schema besturing RC auto](./schema%20besturing%20rc%20auto.sch): Dit is het schema van besturing.

## uitleg code

Beide codebestanden kunnen gebruikt worden voor het stuur en de pedalen aan te sturen.
Hierbij wordt er een spanning, die verkregen wordt door het bewegen van stuur of indrukken van pedalen, omgezet naar een PWM signaal naar de auto die op zijn beurt het signaal verwerkt.

Autostart.md is een uitleg voor de code op de achtergrond te laten draaien van de pi bij het opstarten.

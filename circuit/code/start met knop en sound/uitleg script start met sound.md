# Installatiehandleiding voor het script "start met sound.py"

Dit document legt uit hoe je het script kunt installeren en gebruiken om de NeoPixel-LED-strip en geluidseffecten te bedienen met een knop.

## Benodigdheden

1. **Hardware**:
   - Raspberry Pi (met GPIO-ondersteuning)
   - NeoPixel-LED-strip (aangesloten op GPIO pin 18, 5V en ground van de Raspberry Pi)
   - Drukknop (aangesloten op GPIO pin 7 en ground van de Raspberry Pi)
   - Audio-uitgang:
     - Via HDMI naar een scherm met ingebouwde speakers

2. **Software**:
   - Raspbian OS (of een andere Linux-distributie voor de Raspberry Pi)
   - Python 3
   - Vereiste Python-bibliotheken:
     - `pygame`
     - `rpi.gpio`
     - `neopixel`

---

## Installatie

1. **Virtuele omgeving aanmaken**:
   Maak een virtuele omgeving aan om afhankelijkheden te beheren:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

---

2. **Python en vereisten installeren**:
   Open een terminal op je Raspberry Pi en voer de volgende commando's uit:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip -y
   pip3 install pygame rpi.gpio adafruit-circuitpython-neopixel
   ```

---

3. **Dependencies uitvoeren**:
   Zorg ervoor dat je alle benodigde bibliotheken installeert door het volgende commando uit te voeren:

   ```bash
   pip3 install -r dependencies.txt
   ```

   **Opmerking**: Zorg ervoor dat het bestand `dependencies.txt` de juiste afhankelijkheden bevat.

    ```bash
    Adafruit-Blinka==8.55.0
    adafruit-circuitpython-busdevice==5.2.11
    adafruit-circuitpython-connectionmanager==3.1.3
    adafruit-circuitpython-neopixel==6.3.15
    adafruit-circuitpython-pixelbuf==2.0.7
    adafruit-circuitpython-requests==4.1.10
    adafruit-circuitpython-typing==1.11.2
    Adafruit-PlatformDetect==3.77.0
    Adafruit-PureIO==1.1.11
    binho-host-adapter==0.1.6
    pyftdi==0.56.0
    pyserial==3.5
    pyusb==1.3.1
    rpi-ws281x==5.0.0
    RPi.GPIO==0.7.1
    sysv-ipc==1.1.0
    typing_extensions==4.12.2
    ```

---

4. **Script downloaden**:
   Plaats het bestand `start met sound.py` in een map op je Raspberry Pi. Zorg ervoor dat de geluidsbestanden `smal_Beep.wav` en `long_beep.wav` zich in dezelfde map bevinden als het script.

---

5. **Hardware aansluiten**:
   - Sluit de NeoPixel-LED-strip aan op GPIO pin 18, de 5V pin en de ground pin van de Raspberry Pi.
   - Sluit de drukknop aan op GPIO pin 7 en de ground pin van de Raspberry Pi.
   - Sluit een speaker of koptelefoon aan op de audio-uitgang van het aangesloten scherm.

---

6. **Audio-uitgang instellen**:
   - Gebruik de terminal om de audio-uitgang in te stellen:
  
     ```bash
     sudo raspi-config
     ```

     Ga naar `Advanced Options > Audio` en selecteer de gewenste audio-uitgang.
   - Of stel de audio-uitgang in via de GUI van Raspbian:
     - Klik op het luidsprekerpictogram in de taakbalk.
     - Selecteer de gewenste audio-uitgang ( HDMI ).

---

1. **Script uitvoeren**:
   Zorg ervoor dat je in de virtuele omgeving bent door het volgende commando uit te voeren:

   ```bash
   source venv/bin/activate
   ```

   Navigeer vervolgens naar de map waar het script zich bevindt en voer het uit met:

   ```bash
   sudo python3 "start met sound.py"
   ```

---

## Gebruik

- Zodra het script draait, zie je de boodschap: `Ready - Druk op de knop (PIN7) om te starten...`.
- Druk op de knop om de LED- en geluidsequentie te starten.
- Het script speelt korte piepjes af terwijl het LED-segmenten aanstuurt, gevolgd door een lange piep.

## Stoppen

- Druk op `Ctrl+C` in de terminal om het script te stoppen.
- Het script schakelt automatisch de LEDs uit en sluit de GPIO-pinnen en audio af.

---

## Probleemoplossing

- **Geen geluid**:
  - Controleer of de geluidsbestanden `smal_Beep.wav` en `long_beep.wav` correct zijn geplaatst.
  - Controleer of de audio-uitgang correct is ingesteld (HDMI of 3.5 mm jack).
  - Stel de audio-uitgang in via het Raspberry Pi-configuratiemenu of de GUI (zie stap 6).

- **LEDs werken niet**: Controleer de verbindingen van de NeoPixel-LED-strip en zorg ervoor dat de juiste GPIO-pin is ingesteld (standaard GPIO 18).

- **Knop werkt niet**: Controleer de bedrading van de knop en zorg ervoor dat deze is aangesloten op GPIO pin 7 en de ground pin van de Raspberry Pi.

Met deze stappen zou je het script succesvol moeten kunnen installeren en gebruiken!

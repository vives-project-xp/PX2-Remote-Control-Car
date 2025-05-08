# Opties voor het bedraden van de WS2812B naar de Raspberry Pi

Er zijn meerdere opties voor het bedraden van WS2812B naar de Raspberry Pi , afhankelijk van uw omstandigheden.

Wat het meeste vorkomt , is dat de **Raspberry Pi GPIO -pinnen 3.3V** geven op de output en de **WS28XX LED -strips 5V** nodig hebben.

Controleer de specificaties van uw product.
  
De meest betrouwbare manier om dit op te lossen is met een logische niveauomvormer.
  
We kijken naar verschillende opties hieronder.

## WS2812B Raspberry Pi Bedrading met behulp van een level-shifter chip

Een eenvoudige manier om de WS2812B te verbinden met de Raspberry Pi Veilig is het gebruik van een level-shifter.

 Deze komen ook als kleine boards voor eenvoudige projecten.

 Deze chip schakelt de spanning van **3,3 V** naar de **5V** die nodig is door de adresseerbare LED -strips zonder de PI-GPIO pinnen te beschadigen.

**De bedrading is als volgt:**

- Raspberry Pi GPIO PIN 18 tot 74AHCT125 LLC PIN 1A
- 74AHCT125 LLC PIN 1Y TO WS2812B Gegevens in (DIN)
- Voedingsstroom tot 74AHCT125 LLC Ground
- Voedingsstroom tot 74AHCT125 LLC Pin 1OE
- Voedingsstroom naar Pi Ground (GND)
- Voedingsvoeding tot WS2812B grond (GND of -)
- Voeding 5V tot 74AHCT125 LCC VCC (of +)
- Voeding 5V tot WS2812B 5V (of +)
- Raspberry Pi Bedrading met diode

![met een level shifter.jpg](<pi led configuraties/met een level shifter.jpg>)

## Een andere optie om de PI te isoleren en te beschermen is om een ​​diode te gebruiken

**Dit zou als volgt worden aangesloten:**

- Raspberry Pi GPIO PIN 18 tot WS2812B Gegevens in (DIN)
- 1N4001 diodekathode (zijde met de streep) tot WS2812B 5V (of +)
- **Stroomvoorziening GND** naar **Raspberry Pi GND** (of 0)
- **Voeding GND** tot **WS121812B GND** (GND of -)
- Voeding 5V tot 1N4001 diode -anode (zijkant zonder de streep; zorg ervoor dat u de oriëntatie van de diode correct krijgt, met de kathode (zijkant met de streep) anders kunt u de pi beschadigen)

![bedraad met diode en externe voeding.jpg](<pi led configuraties/bedraad met diode en externe voeding.jpg>)

## Externe stroombron gebruiken zonder te level-schigten op de Raspberry Pi

Het is mogelijk  om WS2812B LED -strips te bedienen zonder te level-shiften.

Ik raad het niet aan, maar in de meeste gevallen als je voorzichtig bent, komt alles goed.

Er zijn echter enkele WS21812B LED -strips die niet zal werken zonder een niveau shifter.

Als je in de problemen komt, moet je er een toevoegen.

**Zonder een logisch niveau shifter zou het zo zijn bedraad:**

- Raspberry Pi Grond (GND) naar WS2812B grond (GND of -)
- Raspberry Pi GPIO PIN 18 tot WS2812B Gegevens in (DIN)
- Voedingsvoeding tot WS2812B grond (GND of -)
- Voeding 5V tot WS2812B 5V (of +)

![externe voeding zonder level shifter.jpg](<pi led configuraties/externe voeding zonder level shifter.jpg>)

## WS2812B rechtstreeks vanuit Raspberry Pi Zonder niveau te verschuiven

De laatste optie werkt alleen met een kleine aantal LED's.

 Controleer de specificaties op uw adresseerbare LED -strips om te controleren hoeveel stroom nodig is en zorg ervoor dat  het aantal LED's de  **Raspberry Pi** Maximale stroomlimiet van **51 milliamp** niet overschrijdt.

 **Bedradingsschema is als volgt:**

![rechtstreeks op pi.jpg](<pi led configuraties/rechtstreeks op pi.jpg>)

- Raspberry Pi 5V tot WS2812B 5V (of +)
- Raspberry Pi GND naar WS2812B grond (GND of -)
- Raspberry Pi GPIO PIN 18 tot WS2812B Gegevens in (DIN)

[thegeekpub](https://www.thegeekpub.com/15990/wiring-ws2812b-addressable-leds-to-the-raspbery-pi/?srsltid=AfmBOopCNNKBqP1UMyui9dj0vG7H8_cM-HufnEJjs7s2CZ9avXvwOOD3)

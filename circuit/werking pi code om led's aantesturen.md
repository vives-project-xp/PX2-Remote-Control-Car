# Installatie van de neopixelbibliotheek voor Python

Er zijn verschillende bibliotheken voor het besturen van WS2812B LED's met een Raspberry Pi, men kan dit doen door bv. de neopixelbibliotheek te gebruiken.

Het is super eenvoudig te gebruiken

## Voer de volgende opdracht uit om de neopixelbibliotheek te installeren

```bash
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
```

**Opmerking:**

als u geen verse installatie van python gebruikt.
kan dit ervoor zorgen dat dit niet goed werkt !!

Circuit Python is alleen compatibel met Python 3.x

## Het beheersen van WS2812B LED's met een Raspberry Pi via Python

De eerste paar code -regels in  Python -programma zijn er gewoon om de benodigde bibliotheken te importeren en de WS2812B LED -strip toe te wijzen aan een GPIO -pin.

De volgende code doet dat.
We wijzen **GPIO Pin 18** toe als de verbinding voor onze adresseerbare LED's en we definiëren dat er **30 LED's** in onze strip zijn.

Als uw WS2812B LED -strip langer of korter is, verander dan **30** in het juiste aantal LED's.

```python
1 | import board
2 | import neopixel
3 | pixels = neopixel.NeoPixel(board.D18, 30)
```

dit is het enig dat nodig is!

we kunnen nu alles doen wat we willen.

Laten we gewoon een enkele regel code doen om de eerste LED te verlichten en rood te maken.

Voer de volgende code in en voer vervolgens uw Python -programma uit:

```python

1 | pixels[0] = (255, 0, 0)
```

### Bij uitvoering moet uw adresseerbare LED-strip er de volgende afbeelding uitzien

![ledstrip rood.jpg](<pi led configuraties/ledstrip rood.jpg>)

Het schrijven van een voorlus of het doen van de loop en het wijzigen van een van de cijfers zal de LED's natuurlijk veranderen volgens uw lusverklaring. De volgende code zou bijvoorbeeld de tweede tot tiende LED's in volgorde 1 seconde uit elkaar laten verlichten (we beginnen bij nul en eindigen bij 9 omdat adresseerbare LED's beginnen bij LED 0).

```python

1 | for x in range(0, 9):
2 |    pixels[x] = (255, 0, 0)
3 |    sleep(1)
```

Natuurlijk is het veranderen van de kleur net zo eenvoudig als het wijzigen van de RGB -waarden na pixels (of GRB afhankelijk van uw strips).

Pixels [0] = (0,0,255) zou bijvoorbeeld helderblauw zijn.

 Als u niet bekend bent met RGB, moet een eenvoudige Google-zoekopdracht u op de juiste weg instellen, maar simpelweg 0-255 Definieert de helderheid of intensiteit van de LED-kleur in rood, groen of blauw.

Als u de hele LED -strip aan wilt zetten en alle LED's op Green instelt, zouden we het vulopdracht gebruiken om dat te doen:

```python

1 | pixels.fill((0, 255, 0))
```

![ledstrip groen.jpg](<pi led configuraties/ledstrip groen.jpg>)

# Arduino Code voor LED-strip Besturing via ESP

Deze Arduino code is ontworpen om een LED-strip aan te sturen met behulp van een ESP-module. De code maakt gebruik van de Adafruit NeoPixel bibliotheek om de LED-strip te bedienen. De LED-strip is verdeeld in secties, en de gebruiker kan een drukknop gebruiken om een sequentie van lichten te activeren, vergezeld van een buzzer die geluid maakt.

## Belangrijke Componenten

- **LED_PIN**: De pin waarop de data van de LED-strip is aangesloten.
- **NUM_LEDS**: Het totale aantal LEDs in de strip.
- **SEGMENT_COUNT**: Het aantal secties waarin de LED-strip is verdeeld.
- **SPACE_BETWEEN**: Het aantal LEDs dat tussen de secties zit.
- **SEGMENT_SIZE**: Het aantal LEDs per sectie.
- **BUTTON_PIN**: De pin waarop de drukknop is aangesloten.
- **BUZZER_PIN**: De pin waarop de buzzer is aangesloten.

## Functionaliteit

1. **Setup**: In de `setup()` functie worden de LED-strip en de pinnen voor de drukknop en buzzer geconfigureerd. De LED-strip wordt in de beginstatus uitgeschakeld.
  
2. **Loop**: In de `loop()` functie wordt continu gecontroleerd of de drukknop is ingedrukt. Wanneer de knop wordt ingedrukt:
   - Wordt elke sectie van de LED-strip één voor één rood verlicht, met een korte pauze tussen elke sectie.
   - De buzzer maakt een geluid terwijl de secties worden verlicht.
   - Na het verlichten van alle secties, blijft de buzzer aan en worden de LEDs voor een willekeurige tijd (tussen 0.2 en 3 seconden) ingeschakeld.
   - Vervolgens worden alle LEDs uitgeschakeld en stopt de buzzer.

3. **Knopstatus**: De status van de drukknop wordt bijgehouden om te voorkomen dat de cyclus meerdere keren wordt gestart bij één druk op de knop.

## Code

```cpp
#include <Adafruit_NeoPixel.h>

#define LED_PIN 13       // Data pin
#define NUM_LEDS 125    // Aantal LEDs
#define SEGMENT_COUNT 5 // Aantal secties
#define SPACE_BETWEEN 8 // Aantal LEDs tussen de secties 
#define SEGMENT_SIZE 17 // Aantal LEDs per sectie 
#define BUTTON_PIN 15   // Pin drukknop
#define BUZZER_PIN 21   // Pin buzzer

Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRBW + NEO_KHZ800);

bool buttonPressed = false;  // Status drukknop 

void setup() {
  strip.begin();
  strip.show(); // Zet alle LEDs uit
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Zet de knop in als input met pull-up weerstand
  pinMode(BUZZER_PIN, OUTPUT); // Zet de buzzer pin als output
}

void loop() {
  // Controleer of de knop is ingedrukt 
  if (digitalRead(BUTTON_PIN) == LOW && !buttonPressed) {
    buttonPressed = true;  // Zet de knopstatus op ingedrukt
    
    // Deel de LED-strip op in 5 secties, met ruimte ertussen. 
    for (int i = 0; i < SEGMENT_COUNT; i++) {
      // Zet het huidige segment op rood (startlicht aan)
      for (int j = i * (SEGMENT_SIZE + SPACE_BETWEEN); j < (i + 1) * SEGMENT_SIZE + i * SPACE_BETWEEN; j++) {
        strip.setPixelColor(j, strip.Color(255, 0, 0, 0)); // Rood
      }
      strip.show();
      
      // Laat de buzzer een geluid maken
      tone(BUZZER_PIN, 1000, 200); // Buzzer speelt 1000Hz voor 200ms
      delay(1000); // Wacht 1 seconde tussen de secties
    }

     // Zet de buzzer AAN terwijl alle lampen rood zijn
    tone(BUZZER_PIN, 1000); 

    // Wacht willekeurige tijd (tussen 0.2 en 3 seconden) 
    int randomDelay = random(200, 3000);  // random waarde tussen 200 ms en 3000 ms  
    delay(randomDelay);  // Wacht de willekeurige tijd
    
    // Zet alle LEDs tegelijk uit
    for (int i = 0; i < NUM_LEDS; i++) {
      strip.setPixelColor(i, strip.Color(0, 0, 0, 0)); // Uit
    }
    strip.show();
    
    // Stop de buzzer
    noTone(BUZZER_PIN); // Stop geluid van buzzer
  }

  // Zet buttonPressed terug naar false wanneer de knop wordt losgelaten, zodat de cyclus opnieuw kan starten
  if (digitalRead(BUTTON_PIN) == HIGH) {
    buttonPressed = false;
  }
}

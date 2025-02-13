# Voeding

## bedoelingen 
-  voor de camera
-  esp32
- stappenmotor

## Mogelijke oplossing
Is door gebruik te maken van een zelfgemaakte batterypack of een batterij met een hogere spanning hoeveel deze zou bedragen kan je vrij in zijn maar hiervoor zou ik eerst nog een paar test doen met de camera van hoe hoger het vermogen is wat dan de range van de camera met de bril is. 

## Problemen
Stel dat we gebruik maken van een battery pack van 20V dan zal dit veel te veel zijn voor de esp32 en de stappenmotor. Want de esp32 word via usb met 5V gevoed en de stappenmotor zijn voedingsspanning hangt af van welke voedingspanning je gebruikt. 

## oplossing 
- Lineare spanningsregelaar
- weerstanddeler
- Dc-Dc module
- zenerdiode

### Lineare spanningsregelaar
 Hiervan kan je een op voorhand gemaakt component voor gebruik namelijk 7805 of LM317. Deze componenten zetten de overtolige spanning om in warmte. Natuurlijk zul je ook nog een paar extra componenten moeten toevoegn voor de schakeling van afhankelijk hoeveel spanning je op je uitgang wilt. 
 ![spanningsregelaar](/Video/afbeeldingen/maximum%20rating%207805.png)
 ![7805](/Video/afbeeldingen/7805-IC.jpg)

### weerstanddeler
Je kan ook gebruik maken van 2 weerstanden waardoor je een spanningsdeler kan maken. 
Dit wordt bepaalde door de formule: 
$Vo=Vin*R2/R1+R2$
Dit is een zeer eenvoudige oplossing maar er moet wel rekening worden gehouden met de stroom. 
![weerstanddeler](/Video/afbeeldingen/voltage-divider-main-circuit.webp)

### Dc-Dc module
Dit werkt op het zelfde princiepe zoals de lineare spanningsregaal maar hiervoor zou je geen Pcb meer moeten maken omdat het een kant en klaar bordeje is dat je gwn kan kopen. 
![Lm2596](/Video/afbeeldingen/Dc-Dc%20module.png)


### zenerdiode
Werkt een beetje op hetzelfde princiepe van een weerstanddeler maar hiervoor gebruik je een zenerdiode waar een een bepaalde spanningsval over zet in combinatie met een weerstand. Natuurlijk kun je deze ook vervangen door gewone leds en dat je dan deze op de auto zet als extra maar hiervoor zal je wel zeker de stroom in rekening moeten houden die de camera,esp32 en stappenmotor zou kunnen trekken. 
![zenerdiode](/Video/afbeeldingen/zenerschakeling.gif)

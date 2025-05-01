# Voeding

## bedoelingen

- voor de camera
- esp32(mogelijkheid)
- stappenmotor(mogelijkheid)

## Mogelijke oplossing

Is door gebruik te maken van een zelfgemaakte batterypack of een batterij met een hogere spanning hoeveel deze zou bedragen kan je vrij in zijn maar hiervoor zou ik eerst nog een paar test doen met de camera van hoe hoger het vermogen is wat dan de range van de camera met de bril is.

## Gekozen oplossing

We hebben gekozen om een bosh 12V accupack te gebruiken. We zouden deze gebruiken omdat die batterijen ook nog in andere projecten kunnen gebruiken.

![Bosch batterij](/Video/afbeeldingen/Bosh%20batterij.jpg)

Voor die batterij moesten we ook nog een adapter voorzien om mooi de spanning te kunnen aftapen en hiervoor maken we gebruik van een adapter van bosch zelf.

![Bosch adapter](/Video/afbeeldingen/Bosch%20adapter.jpeg)

De batterij kan een spanning van 12V leveren en 3Ah.

## Elektrisch schema

![elektrisch schema](/Video/afbeeldingen/elektrische%20schema.png)

![voeding camera](/Video/afbeeldingen/voeding%20camera.jpg)

![voeding totaal](/Video/afbeeldingen/voeding%20totaal.jpg)

We maken gebruik van een parrallele schakeling want bij parallel is de spanning overal gelijk. Maar de stroom is wel verschillent.
I_totaal=I_camera+I_ventillator=271mA+50mA=321mA

P_totaal=I_totaal*U_bat=321mA*12V=3,852W

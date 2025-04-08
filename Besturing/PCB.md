## Pcb maken 
Doelstelling: 
Alles van de besturing op 1 Pcb zetten.

We hebben dan een deel van de besturing die we laten zoals het is. Dit deeltje zullen we dan "BlackBox" noemen. We zullen er voor zorgen dat we dit op onze eigen PCB kunnen connecteren met Pinheaders (Male, Female). In volgende foto kan je zien wat we als blackbox gebruiken voor het maken van dezze PCB.

![BlackBox](Images/BlackBox.png)

Voor onze PCB moeten we onze blackbox maken in EAGLE zodat we een beeld hebben van hoe we onze componenten op de pcb kunnen plaasten en waar precies zodat we genoeg plaats hebben. 
We zullen dus onze blackbox moeten afmeten en inspecteren van welke pinnen er nu precies gebruikt worden zodat we weten welke we nu allemaal moeten plaatsen in onze tekening

![zelf getekende footprint](Images/Footprint_BB.jpg)

Met deze tekening kunnen we beginnen met onze footprint voor de BlackBox. Ik heb het afgemeten met een schuifmaat voor meer precisie te hebben.

In volgende foto zal je zien dat we nu een footprint hebben getekend met de nodige afmetingen zodat je zeker kan zien en weten  hoe je het moet tekenen. We hebben dit getekend aan de hand van de afmetingen die we op voorhand hebben genomen.

![Footprint die we op eagle hebben getekend](Images/Footprint_BB_eagle.png)

Eenmaal je een footprint hebt moet je ook nog een symbol maken die erbij past. Hiervoor kijk je best eens naar het gene die op de blackbox is geconnecteerd. 

![BB pinnen aantonen die we nodig hebben ](Images/BB_Pinnen.png)

De pinnen die zijn aangeduid in het **rode oppervlak** zijn de pinnen voor de batterij die is aangesloten.
De pinnen met de **gele omranding** zijn de pinnen die ervoor zorgen dat de auto kan sturen en vooruit , achteruit kan rijden.
De pinnen die in de **groene omranding** zit zijn de pinnen die we gebruiken voor het stuur in te stellen op perfectie zodat de auto niet naar links of recht rijd uit zichzelf, het is ook voor een reset knop, we kunnen ook weten als het nog genoeg voeding krijgt door twee leds die er op zitten (groen en rood).

Het Symbol:
![Symbol Eagle](Images/symbol.png)
Je kan dus zien dat ik mijn symbol een beetje heb gemaakt zoals mijn blackbox zelf zodat je beter weet waar je wat moet aan verbinden voor later.

Nu moeten we nog de Footprint en het Symbol verbinden met elkaar en connecteren.
![Footprint en symbol connecteren](Images/Symbol_en_Footprint_connecten.png)

Het beste dat je kunt doen is al je pinnen van op de Footprint en de pinnen van de Symbol dezelfde naamgeving geven zodat je makkelijker weet welke pinnen je nu precies moet verbinden met elkaar. ***(Zoals je ziet in de afbeelding)***

Eenmaal je dit hebt gedaan ben je klaar met de BlackBox. We kunnen nu beginnen met de PCB zelf en dan later gebruik maken van onze BlackBox.

Wat zullen we nu op de PCB zelf plaatsen van compenenten.
We zullen eerst een deeltje van de controller opnieuw maken in onze PCB zodat we minder draden hebben en dus minder slecht contact.

![extra deel van controller](Images/eigenPCB.png)

Voor deze Pcb opnieuw te maken hebben we 4 nieuwe componenten nodig namelijk
- 2x led (Groen en Rood)
- pottentiometer (100kOhm)
- drukknop

De led heeft 3 pinnen maar we zullen gebruik maken van twee Leds in plaats van één. Dan brand er een lichtje als hij aan staat of als de batterij bijna plat is word de led rood. 

Eenmaal we weten welke componenten we nodig hebben voor dit deeltje gaan we verder naar het volgende deeltje van de PCB.

Namelijk een **RC-Filter :**

![RC-Filter](image.png)

![Schakeling voor onze controller](image-1.png)

Zoals je kan zien maken we gebruik van twee RC-Filters omdat we bij beide inputs één nodig hebben. We krijgen dus twee inputs namelijk "het stuur" en "de pedalen".

We zullen nu eerst eens onze componenten zoeken.  
Ik zal deze in een BOM-List plaatsen.

| Component    | Naam  |Waarde  | Library (Eagle) | Beschrijving         |
|--------------|---------|---------|---------------|-------------------|
| Weerstand    | R1| 1kΩ    | rcl (R0603) | Gebruikt in RC-filter|
| Weerstand    | R2| 1kΩ    | rcl (R0603) | Gebruikt in RC-filter|
| Condensator  | C1| 10µF   | rcl (C1210) | Voor signaal filtering|
| Condensator  | C2| 10µF   | rcl (C1210) | Voor signaal filtering|
| Rode Led  | Rled| ------| led | Aantonen batterij niveau controller|
| Groene Led | Gled| ------| led | Aantonen batterij niveau controller|
| Drukknop | S1| ------| switch-omron| Wordt gebruikt als reset|
| 40 female pins| J1| ------| PPPC202LFBN-RC| Connector met PI 5|
| 6 female pins| J2| ------| 6 pins_target| connectie met BB|
| Batterij| BAT| ------| SparkFun-Connectors| Connectie met batterij|
| 3 pins stuur| ST| ------| SparkFun-Connectors| Connectie met BB|
| 3 pins throttle| TH| ------| SparkFun-Connectors| Connectie met BB|
| Ground| GND| ------| supply1| 

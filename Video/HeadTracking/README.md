# Headtracking

## Onderzoek

### Headtracking goggles

De Walksnail Avatar HD goggles X, die we gebruiken voor het project, heeft een headtracking functie die bestaat uit een ingebouwde negen-assige gyroscoop. Deze detecteert de hoofdbewegingen die dan kunnen doorgestuurd worden naar de camera.

### Versturen gegevens goggles naar camera

Die gegevens worden via een digitaal transmissiesysteem naar de camera worden gestuurd.

### Pan- en tilt-systeem

Voor de headtracking zelf kan er gebruik gemaakt worden van een pan- en tilt-systeem om de camera in de juiste positie te krijgen.
Deze kan aangekocht worden of zelf gemaakt met behulp van 2 servomotors en 3D prints. Het signaal dat de goggles zenden is een PPM signaal wat omgevormd zal moeten worden naar een PWM signaal voor de servomotors. Dit kan met behulp van een flight controller, een PPM naar PWM decoder of een microcontroller.

### Servomotor

De SG90 servomotor zou sterk genoeg zijn voor het pan- en tilt-systeem aangezien we geen grote camera hebben.

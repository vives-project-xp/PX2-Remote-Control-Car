# Communicatie tussen bril en camera

We maken gebruik van de Avatar HD Goggles X(bril) en de Avatar HD Pro Kit(camera.)

De communicatie werkt eigenlijk via digitale draadloze verbinding op de 5,725-5,850 Ghz frequentie band. Deze verbinding maakt gebruik van geavanceerde H.265 encoderingtechnologie om 1080p video met maximaal 100 frames per seconde en een gemiddelde vertraging van 22 milliseconden. 

## Beelden doorsturen

### Camera &rarr; VTX

De camera zet het optische beeld om in een digital videostroom. Dit wordt via een datakabel(MIPI-interface) naar de VTX gestuurd.

### VTX verwerkt en verzendt

De VTX codeert het beeld met H.265 compressie om de benstandsgrootte te verkleinen. 
Daarna zet de VTX het signaal om in een draadloos RF-signaal op de 5,8GHz-band en verzendt het naar de bril.

### Bril ontvangt en decodeert

De Avatar HD Goggles X ontvangt het signaal en decodeert het met een ingebouwede H.265-chipt. 
Het beeld wordt weergegeven op de OLED-schermen in de bril. 

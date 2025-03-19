# Ontwerp Start-Finish Systeem
![ontwerp](./research/afb/ontwerp1.png)
![ontwerp](./research/afb/ontwerp2.png)
![ontwerp](./research/afb/ontwerp3.png)

## Benodigdheden:
- **Twee buizen** voor de pilaren (keuze materiaal?)
- **Lange plaat** waar alles kan aan bevestigd worden (hout)
- **Piezo-sirene (12V of 24V)** – Veel luider dan een standaard buzzer en geschikt voor een race-ervaring.

![sirene](./research/afb/Piezo-sirene%20.jpg)
- **Led strip of 5 lampen / leds**
- **Drukknop**
- **UHF RFID-lezer (860-960 MHz, UART/USB)**  
  Geschikt voor grotere afstanden (1-10 meter, afhankelijk van de antenne). Kan meerdere tags tegelijk lezen (handig als er meerdere auto's dicht bij elkaar rijden). Vereist UHF RFID-tags, die iets duurder zijn dan de standaard 13.56 MHz-tags.

  **JRD-4035 Lezermodule 840MHz ~ 960MHz (reader):**
  ![reader](./research/afb/RFID-Lezer.png)
  ***Product features***:  
  * Stabiele herkenningsafstand 1,5m-2m , 
  * Bereik werkspectrum: 840-960MHz ,
  * UART-communicatie-interface (baudrate: 115200bps)
  * Het buffergebied kan tot 200 tags bevatten
  * Tagherkenning is gevoelig en stabiel

  ***Pin mapping***:![pins](./research/afb/PinMappingReader.png)

  **UHF RFID Tags:**

  ![Tags](./research/afb/Tag%20voor%20RFID.png)
  
  ***Product features***
  * Chip: Higgs-EC
  * User Memory: 128bits
  * EPC Memory: 128bit 
  * TID: 96bits 
  * Reserved 64bits  
  * Frequency 860~960MHz (UHF) 
  * Size 30*16mm 
  * Read Range 0~6m (depend on reader)
- **2 led matrixen** (hebben we)
- **Raspberry Pi** (hebben we)


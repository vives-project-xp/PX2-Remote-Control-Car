# handleiding voor dummy's

## 🕹️  1. Stuur en Pedalen

### Benodigdheden

- Raspberry Pi met stroomadapter

  ![Raspberry pi](/Handleidingen/Images/Raspberry%20PI%204.jpg)

- Stuur en pedalen set

  ![stuur en pedalen](/Handleidingen/Images/Logitech_G923.webp)

- Meegeleverde stroomadapter voor de pedalen
- USB-kabel van het stuur

### Stappen

1. Raspberry Pi van stroom voorzien :

   Sluit de Raspberry Pi aan op een stopcontact met de bijgeleverde stroomadapter en wacht tot het systeem is opgestart.

2. Pedalen aansluiten :

   Verbind de pedalen met het stuur en sluit ze aan op de meegeleverde stroomadapter.

3. Stuur verbinden :

   Steek de USB-kabel van het stuur in een beschikbare USB-poort van de Raspberry Pi.

## 📷 2. Bril en Camera

### Benodigdheden

- Bril met meegeleverde batterij en 3D-geprint harnas

![fpv bril](/Handleidingen/Images/Walksnail%20Avatar%20HD%20Goggles%20X.png)

- Camera (details in hoofdstuk 'Auto')
- Video-compiler
- Dun staafje

### Stappen

1. Bril voorbereiden :

   Voorzie de bril van stroom met de meegeleverde batterij en berg deze netjes op in het bijgeleverde 3D-geprinte harnas

   ![bril batterij](/Handleidingen/Images/batterij%20camera.webp)

2. Camera van stroom voorzien :

   Sluit de camera aan op stroom (raadpleeg het hoofdstuk 'Auto' voor meer details).

3. Video-compiler activeren :

   Druk kort op de knop van de video-compiler totdat de rode LED begint te knipperen.

   ![compiler knop](/Handleidingen/Images/zender_camera.jpg)

4. Koppeling starten :

   Druk met een dun staafje op de 'Link'-knop van de bril. Je hoort een korte pieptoon.

   ![paring knop](/Handleidingen/Images/fpv_bril_top_pairing.png)

5. Koppeling voltooien :

   Wacht tot de pieptoon stopt en het LED-lampje op de video-compiler groen oplicht. (ongeveer 8 sec)

   De bril en camera zijn nu gekoppeld, waardoor je het camerabeeld via de bril kunt bekijken.

---

## 🚗 3. Auto

### Benodigdheden

- Auto met plastic paneel
- Harnas voor de camera
- Camera met foam
- Video-compiler
- Ventilator
- Bosch-batterij
- Autobatterij

### Stappen

1. Plastic paneel verwijderen :

   Haal het plastic paneel van de auto door de twee clips aan de voor- en achterkant los te maken.

2. Harnas plaatsen :

   Bevestig het harnas voor de camera aan de voorkant van de auto, ter hoogte van het daarvoor gemaakte gat in het plastic paneel.

3. Camera installeren :

   Plaats de camera van bovenaf in het voorziene gat en voeg de bijgeleverde foam toe.

4. Video-compiler monteren
   Monteer de video-compiler aan de achterkant van het harnas in het daarvoor bestemde gat.

5. Ventilator bevestigen :

   Bevestig de ventilator op de vier uitstekende pinnen aan de achterzijde.

6. Stroomvoorziening aansluiten :

   Sluit de video-compiler en de ventilator aan op de Bosch-batterij.

7. Autobatterij plaatsen:

   Plaats de autobatterij op de daarvoor bestemde plek in de auto.

8. Auto inschakelen :

   Schakel de auto in. (Zorg dat dit gebeurt voordat je het plastic paneel terugplaatst, zodat de auto functioneel is.)

9. Plastic paneel terugplaatsen :

   Bevestig het plastic paneel terug op de auto.

---

## 💻 4. Start/finish systeem

### Benodigdheden

- Monitor met stroomadapter
- HDMI-kabel (mini HDMI naar HDMI)
- Raspberry Pi met stroomadapter
- Toetsenbord en muis

Verbinding met een terminal

### Stappen

1. Monitor aansluiten
   Voorzie de monitor van stroom en sluit de HDMI-kabel aan (van mini HDMI naar HDMI).
2. Raspberry Pi voorbereiden :

   Voorzie de Raspberry Pi van stroom.

   ![pi_power](/Handleidingen/Images/voeding_pi.png)

3. Input-apparaten verbinden :

   Sluit een toetsenbord en muis aan op de USB-poorten van de Raspberry Pi.

   ![IO_PI](/Handleidingen/Images/IO_PI.png)

4. opstarten en terminal openen :

   Wacht tot de Raspberry Pi volledig is opgestart en open daarna de terminal.

5. Navigeren naar de 'circuit' folder :

   Ga naar de folder 'circuit' in je bestandsstructuur.

   ***let wel op dat je dit runt in een virtuele omgeving "venv" die de nodige requirements reeds heeft.***

   ***terug te vinden in de "requirments.txt" file***

6. Code laden :

   Voer het commando uit:

   ```sh
   sudo python "Dashboard_lights.py"
   ```

   Hiermee wordt de code op de Raspberry Pi geladen.

---

## 🔧 5. Lichten en knoppen monteren & aansluiten

### Benodigdheden

- LED-lichten
- Drukknoppen
- Bekabeling (jumper wires)
- Raspberry Pi
- Schroevendraaier (indien nodig)
- Frame
- Raspberry Pi-document (voor aansluitinformatie)

### Stappen

1. Plaatsing op het frame :

   Monteer de LED-lichten en knoppen stevig op het bijgeleverde frame. Zorg dat alles goed vastzit en toegankelijk blijft voor gebruik.

2. Kabels voorbereiden :

   Gebruik jumper wires om verbindingen te maken tussen de lichten, knoppen en de GPIO-pinnen van de Raspberry Pi.

3. Aansluiten op de Raspberry Pi :

   Sluit de kabels van de lichten en knoppen aan op de juiste GPIO-pinnen van de Raspberry Pi.
   📘 Raadpleeg het Raspberry Pi-document voor de juiste pin-layout en aansluiting.

4. Controleer de verbindingen :

   Dubbelcheck of alle verbindingen stevig en correct zijn aangesloten. Let op de richting en polariteit van de LED’s.

5. Stroom aansluiten (pas als alles gemonteerd is) :

   Zorg ervoor dat alle hardware goed is aangesloten voordat je de Raspberry Pi van stroom voorziet.

   ![schema](/Handleidingen/Images/aansluitschema_circuit.png)

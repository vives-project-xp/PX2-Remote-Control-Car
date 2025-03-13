
Gaan naar je folder
cd led_strip_project

Je wordt root user: 
sudo su

Maak een nieuwe venv
python -m venv venv

Laad je venv
source venv/bin/activate

Installeer je python libraries
pip install Adafruit-Blinka adafruit-circuitpython-neopixel

Run je script
python test.py

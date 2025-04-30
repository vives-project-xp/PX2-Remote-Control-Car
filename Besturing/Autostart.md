Open terminal van de raspberry pi.
Enter command crontab -e
en voeg de line: "@reboot /usr/bin/python3 /path/to/script.py &" toe.
Dit zorgt ervoor dat wanneer de py opstart dat het de code in de achtergrond loopt.

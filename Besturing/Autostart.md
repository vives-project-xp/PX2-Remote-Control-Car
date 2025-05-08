# Autostart

## Waarom

We gebruiken dit voor het gemakkelijk opstarten van de stuur en pedalen en zodat we geen display, toetsenbord en muis nodig hebben voor de code te laten draaien.

## Gebruiken

Open een terminal in de raspberry pi.
Enter command

```bash
crontab -e
```

Hierdoor krijg je een scherm te zien met de crontab. Dit is een programma dat automatisch taken kan uitvoeren op bepaalde tijdstippen.
Hierin kan je een regel toevoegen die de code automatisch laat draaien bij het opstarten van de raspberry pi.
De regel die je moet toevoegen is:

```bash
"@reboot /usr/bin/python3 /path/to/script.py &"
```

Hierbij moet je de path naar de code aanpassen naar de juiste locatie van de code. Het is belangrijk dat je het pad naar de python interpreter ook aanpast als deze anders is.
Je kan dit controleren door in de terminal het volgende command in te geven:

```bash
which python3
```

Dit geeft je het pad naar de python interpreter. Dit moet je dan ook aanpassen in de regel die je toevoegt aan de crontab.
Je kan de crontab afsluiten door op `CTRL + X` te drukken en dan `Y` in te geven om de wijzigingen op te slaan. Hierna zal de code automatisch draaien bij het opstarten van de raspberry pi.

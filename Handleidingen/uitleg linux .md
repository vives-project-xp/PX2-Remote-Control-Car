# hoe installeer je de nodige omgevingen en libraries in linux

linux heeft met de laatste releases beslist dat om de kernel te beschermen,
men geen pip packages meer kan of mag installeren.

dit om ervoor te zorgen dat linux zelf niet kapot gaat.

men dient vanaf nu steeds een virtuele omgeving te maken de zo genoemde **"venv"**

in deze venv moet men  alle nodige packages installeren als vanouds in linux deze zijn dan enkel van toepassing in deze omgeving.

pip install < packages >

----

men gaat via terminal en met het commando **" cd "** (change directory) naar de gewenste map waar je de omgeving wil in opslaan.

met **"cd .. "** kan je telkens naar de bovenliggende map gaan

----

met de **" ls "** commando (list) toon je de inhoud van de huidige directory.

----

bv project

Gaan naar je folder

````sh
cd project
````

----

Je wordt root user:

````sh
sudo su
````

----

Maak een nieuwe venv

````sh
python -m venv venv
````

----

Laad je venv

```sh
source venv/bin/activate
```

----

Installeer je python libraries
dit kan aan de hand van een eventuele reeds aangemaakte text file zijn (dependencies.txt)

````sh
sudo pip install -r < text.file >
````

----

(pip = python install packages) (-r = read-permission)

Run je script

````sh
pip python < program.py >
````

----

## voorbeeld

![install path](/Handleidingen/Images/install_path.png)

![activate venv](/Handleidingen/Images/activate_venv.png)

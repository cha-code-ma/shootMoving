# shootMoving
In this repository, we will use the Adruino Nano IoT microchip and Python to shoot in the game Half-Life, whenever the person moves the adruino back and forth (shooting motion).
The way shooting is happening is by the python library pyautogui, so this means it just does a mouse click in the center of your sceen, whenever you move the arduino in a shooting motion.


## How to start?
In order to start this program, We first need to Download all the included python packages:

### 1(LINUX):
sudo apt update

sudo apt install python3-pip -y

pip install pyautogui PyQt5 bleak matplotlib

### 2(LINUX): met een virtueel environment:
python3 -m venv venv
source venv/bin/activate
pip install pyautogui PyQt5 bleak matplotlib

### 3(WINDOWS): ook met een virtueel environment:
Hier is een samenvatting van alle stappen om je programma op Windows te draaien:
1. Python installeren
Download en installeer Python via python.org. Vink tijdens installatie "Add Python to PATH" aan (PATH is een systeeminstelling die aangeeft waar je terminal programma's zoals python kan vinden).

2.Download this github in a zip-file and extract this zip-file.

3. Terminal openen
Open Command Prompt (de terminal-programma van Windows waarin je tekst-commando's uitvoert).

4. Venv aanmaken:
python -m venv venv. Dit moet gedaan worden in de `application` folder.

5. Venv activeren:
Command prompt:
venv\Scripts\activate.bat

5.Pakketen instaleren:
pip install pyautogui PyQt5 bleak matplotlib

### Now run this program:
Download the `application` folder and in the terminal, run:
-python -m GUI.main yesgui     --if you want a pyqt5 gui
-python -m GUI.main nogui      --if you only want to use the terminal

good luck!


# shootMoving
In this repository, we will use the Adruino Nano IoT microchip and Python to shoot in the game Half-Life, whenever the person moves the adruino back and forth (shooting motion).


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
2. Terminal openen
Open Command Prompt of PowerShell (de terminal-programma's van Windows waarin je tekst-commando's uitvoert).
3. Venv aanmaken:
python -m venv venv
4. Venv activeren:
Command prompt:
venv\Scripts\activate.bat
powershell:
venv\Scripts\Activate.ps1
5.Pakketen instaleren:
pip install pyautogui PyQt5 bleak matplotlib

### Now run this program:
Download the `application` folder and in the terminal, run:
python -m GUI.main

And you will see a PyQt5 window.


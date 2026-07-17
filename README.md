# shootMoving
In this repository, we will use the Adruino Nano IoT microchip and Python to shoot, walk and turn in the game Half-Life.

You need to position the arduino, so that the charching port is facing you.

You can shoot, by doing a back and forth motion, like shooting a gun with your arduino.

you can turn, by turning your arduino left or right.

you can walk, by tilting your arduino wordward or backwards.

The way shooting is happening is by the python library pyautogui and pydirectinput, so this means it just does a mouse click in the center of your sceen, whenever you move the arduino in a shooting motion.


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
Open Command Prompt as administrator. and because you now start at C:Windows\System32, you need to do:
`cd C:\Users\<your-username>\<path to shootmoving-main>`

5. Venv aanmaken:
python -m venv venv. Dit moet gedaan worden in de `application` folder.

6. Venv activeren:
Command prompt:
venv\Scripts\activate.bat

5.Pakketen instaleren:
pip install pyautogui pydirectinput PyQt5 bleak matplotlib

### Now run this program:
now go to the `application` subfolder and run:

-python -m app.py yesgui     --if you want a pyqt5 gui

-python -m app.py nogui      --if you only want to use the terminal

good luck!


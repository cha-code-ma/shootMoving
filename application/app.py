import sys
import subprocess


if __name__ == "__main__":
    keuze = sys.argv[1]

    if keuze == 'yesgui':
        print("start subprocess")
        subprocess.run(['python', 'GUI/main.py'])
    elif keuze == 'nogui':
        print("start subprocess")
        subprocess.run(['python', 'runTerminal.py'])
    else:
        print("no valid argument")
import sys
import subprocess
import os

if __name__ == "__main__":
    keuze = sys.argv[1]
    basis_map = os.path.dirname(os.path.abspath(__file__))  # directory to map of app.py

    if keuze == 'yesgui':
        print("start subprocess")
        subprocess.run(['python', '-m', 'GUI.main'], cwd=basis_map)
    elif keuze == 'nogui':
        print("start subprocess")
        subprocess.run(['python', 'runTerminal.py'], cwd=basis_map)
    else:
        print("no valid argument")
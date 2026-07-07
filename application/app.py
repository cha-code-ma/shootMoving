import sys
import subprocess

keuze = sys.argv[1]

if keuze == 'yesgui':
    subprocess.run(['python', 'GUI/main'])
elif keuze == 'nogui':
    subprocess.run(['python', ''])
else:
    print("no valid argument")
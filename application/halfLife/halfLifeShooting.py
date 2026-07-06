
"""
Github: cha-code-ma

In this file, we will try to shoot automatically in half-life.

"""
import pyautogui
from time import sleep

class halfLifeManager():


    def shoot(self):
        print("shooting on screen")
        width, heigth = pyautogui.size()
        Xcenter = width // 2
        Ycenter = heigth // 2
        pyautogui.click(Xcenter, Ycenter)
        #sleep(0.1)
        #pyautogui.click(Xcenter, Ycenter)

    def test(self):
        width, heigth = pyautogui.size()
        for _ in range(3):
            pyautogui.click(width - 10, heigth-10)
            print("click")
            sleep(0.2)
        for _ in range(2):
            pyautogui.press('shift')
"""
if __name__ == "__main__":
    manager = halfLifeManager()
    manager.test()
    manager.shoot()
"""
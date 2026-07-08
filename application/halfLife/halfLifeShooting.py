
"""
Github: cha-code-ma

In this file, we will try to shoot automatically in half-life.

"""
import threading
import pyautogui
from time import sleep
from enum import Enum
class direction(Enum):
    LEFT = -1
    RIGHT = 1

class halfLifeManager():

    def __init__(self):
        self.width, self.heigth = pyautogui.size()
        self.Xcenter = self.width // 2
        self.Ycenter = self.heigth // 2


    def shoot(self):
        t = threading.Thread(target=self.shoot_thread)
        t.start()

    def shoot_thread(self):
        pyautogui.click(self.Xcenter, self.Ycenter)
        sleep(0.050)
        pyautogui.click(self.Xcenter, self.Ycenter)

    def turn(self, dir: direction):
        t = threading.Thread(target=self.turn_thread)
        t.start()

    def turn_thread(self, dit:direction):
        print("turning")
        if dir == direction.LEFT:
            pyautogui.moveTo(self.Xcenter, self.Ycenter)
            pyautogui.dragRel(-self.Xcenter// 5, 0, duration=0.1)
            pyautogui.moveTo(self.Xcenter, self.Ycenter)
        if dir == direction.RIGHT:
            pyautogui.moveTo(self.Xcenter, self.Ycenter)
            pyautogui.dragRel(self.Xcenter// 5, 0, duration=0.1)
            pyautogui.moveTo(self.Xcenter, self.Ycenter)

    def test(self):

        for _ in range(3):
            pyautogui.click(self.width - 10, self.heigth-10)
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

"""
Github: cha-code-ma

In this file, we will try to shoot automatically in half-life.

"""
import threading
import pyautogui
from time import sleep
from logic.enums import turningStatus, walkingStatus

class halfLifeManager():
    pyautoguiLock = threading.Lock()


    def __init__(self):
        self.width, self.heigth = pyautogui.size()
        self.Xcenter = self.width // 2
        self.Ycenter = self.heigth // 2


    def walk(self, direct, speed):
        t = threading.Thread(target = self.walk_thread, args=[direct, speed])
        t.start()

    def walk_thread(self, direct, speed):
        with self.pyautoguiLock:
            if direct == walkingStatus.FORWARD:
                pyautogui.keyDown('w')
                sleep(0.5)
                pyautogui.keyUp('w')
            elif direct == walkingStatus.BACKWARD:
                pyautogui.keyDown('s')
                sleep(0.5)
                pyautogui.keyUp('s')


    def shoot(self):
        t = threading.Thread(target=self.shoot_thread)
        t.start()

    def shoot_thread(self):
        with self.pyautoguiLock:
            pyautogui.click(self.Xcenter, self.Ycenter)
            sleep(0.050)
            pyautogui.click(self.Xcenter, self.Ycenter)

    def turn(self, dir: turningStatus):
        t = threading.Thread(target=self.turn_thread, args=[dir])
        t.start()

    def turn_thread(self, direct: turningStatus):
        with self.pyautoguiLock:
            if direct == turningStatus.LEFT:
                pyautogui.moveTo(self.Xcenter, self.Ycenter)
                pyautogui.dragRel(-self.Xcenter// 5, 0, duration=0.1)
                pyautogui.moveTo(self.Xcenter, self.Ycenter)
            if direct == turningStatus.RIGHT:
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
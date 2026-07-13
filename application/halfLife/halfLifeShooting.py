
"""
Github: cha-code-ma

In this file, we will try to shoot automatically in half-life.

"""
import threading
from time import sleep
from logic.enums import turningStatus, walkingStatus
import platform
if platform.system() == "Windows":
    import pydirectinput as input_lib
else:
    import pyautogui as input_lib

class halfLifeManager():
    pyautoguiLock = threading.Lock()

    
    def __init__(self):
        self.width, self.heigth = input_lib.size()
        self.Xcenter = self.width // 2
        self.Ycenter = self.heigth // 2


    def walk(self, direct):
        t = threading.Thread(target = self.walk_thread, args=[direct])
        t.start()

    def walk_thread(self, direct):
        with self.pyautoguiLock:
            if direct == walkingStatus.FORWARD:
                input_lib.keyDown('w')
                sleep(0.5)
                input_lib.keyUp('w')
            elif direct == walkingStatus.BACKWARD:
                input_lib.keyDown('s')
                sleep(0.5)
                input_lib.keyUp('s')


    def shoot(self):
        t = threading.Thread(target=self.shoot_thread)
        t.start()

    def shoot_thread(self):
        with self.pyautoguiLock:
            input_lib.click(self.Xcenter, self.Ycenter)
            sleep(0.050)
            input_lib.click(self.Xcenter, self.Ycenter)

    def turn(self, dir: turningStatus):
        t = threading.Thread(target=self.turn_thread, args=[dir])
        t.start()

    def turn_thread(self, direct: turningStatus):
        with self.pyautoguiLock:
            if direct == turningStatus.LEFT:
                print("TURN LEFT")
                input_lib.moveTo(self.Xcenter, self.Ycenter)
                input_lib.drag(-self.Xcenter // 5, 0, duration=0.4, button='left')
                input_lib.moveTo(self.Xcenter, self.Ycenter)
            if direct == turningStatus.RIGHT:
                print("TURN RIGHT")
                input_lib.moveTo(self.Xcenter, self.Ycenter)
                input_lib.drag(self.Xcenter // 5, 0, duration=0.4, button='left')
                input_lib.moveTo(self.Xcenter, self.Ycenter)

    def test(self):

        for _ in range(3):
            input_lib.click(self.width - 10, self.heigth-10)
            print("click")
            sleep(0.2)
        for _ in range(2):
            input_lib.click('shift')
"""
if __name__ == "__main__":
    manager = halfLifeManager()
    manager.test()
    manager.shoot()
"""
"""
Gemaakt door: Github: cha-code-ma

"""


import logic.detectArduinoNoGUI, logic.detectMotion
from logic.detectMotion import turningStatus, walkingStatus
from halfLife.halfLifeShooting import halfLifeManager
from time import sleep
import threading
import queue
from enum import Enum

AMOUNT_OF_ARDUINO_VALUES = 7
AMOUNT_OF_MOMENTS = 100
AMOUNT_OF_GRAPH_MOMENTS = 30


class shootMoving():
    def __init__(self):
        print("no GUI mode")


        #All variables:
        self.allValues = [[0] for i in range(AMOUNT_OF_ARDUINO_VALUES - 1)]
        #self.varList = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
        self.time = [0]
        self.graphValues = [[0] for i in range(AMOUNT_OF_ARDUINO_VALUES - 1)]


        #BLE communication:
        self.bleComManager = logic.detectArduinoNoGUI.BleCommunicationManager()

        self.q = queue.Queue() #om dezeflde data te kunnen aanpassen zonder racing condition
        self.stopEvent = threading.Event() # simpel vlaggetje om de thread te laten stoppen
        self.thread = threading.Thread(target=self.addValues, args=(self.q, self.stopEvent))

        #Shoot Detection:
        self.movementDetector = logic.detectMotion.movementDetector()
        self.isShooting = False

        #HalfLife:
        self.halfLifeManager = halfLifeManager()


    def start(self):
        self.bleComManager.start_thread(self.q, self.stopEvent)
        try:
            while(1):
                self.loopEvent()
                sleep(0.1)
        except KeyboardInterrupt:
                print("Afsluiten...")
        finally:
            self.stopEvent.set()
            self.thread.join()

    def addValues(self, values):
        if type(values) is bool or len(values) != AMOUNT_OF_ARDUINO_VALUES:
            return None

        for i in range(AMOUNT_OF_ARDUINO_VALUES):
            if i == AMOUNT_OF_ARDUINO_VALUES - 1:
                self.time.append(round(values[i]/1000, 3))
                self.time = self.time[-AMOUNT_OF_GRAPH_MOMENTS:]
                continue

            self.allValues[i].append(round(values[i], 3))
            self.graphValues[i].append(round(values[i], 3))

            self.allValues[i][-AMOUNT_OF_MOMENTS:]
            self.graphValues[i] = self.allValues[i][-AMOUNT_OF_GRAPH_MOMENTS:]


    def chooseValuesIndex(self, index):
        list = []
        for i in range(AMOUNT_OF_ARDUINO_VALUES):
            if i == AMOUNT_OF_ARDUINO_VALUES - 1:
                list.append(self.time[index])
                continue
            list.append(self.allValues[i][index])
        return list

    def movementDetected(self):
        shot, accel = self.movementDetector.isShooting(self.allValues, self.time)
        shot = not self.movementDetector.stopShooting(self.allValues, self.time)
        turning, direc, _ = self.movementDetector.turning(self.allValues, self.time)
        walking, walkSpeed = self.movementDetector.walking(self.allValues, self.time)
        if shot:
            self.isShooting = True
            #print(f"Is shooting: {accel}")

        else:
            self.isShooting = False
            #print(f"Is NOT shooting")

        print(f"gz: {self.allValues[5][-1]}")
        print(f"gx: {self.allValues[0][-1]}")

        if turning == turningStatus.TURNING:
            print("turning")

            self.halfLifeManager.turn(direc)

        if walking != walkingStatus.STANDING:
            print(f"walking: {walking}")
            self.halfLifeManager.walk(walking, walkSpeed)


    def loopEvent(self):
        try:

            data = self.q.get(timeout=0.05)
            #print(f"data:{data}")
            self.addValues(data)

        except queue.Empty:
            pass

        if self.allValues == [[0], [0], [0], [0], [0], [0]]:
            self.isShooting = False

            return None

        self.movementDetected()
        if self.isShooting:
            self.halfLifeManager.shoot()



if __name__ == "__main__":
    SM = shootMoving()
    SM.start()
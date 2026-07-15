import threading
from logic.enums import actionStatus
from halfLife.halfLifeShooting import halfLifeManager
class prioQueue():

    def __init__(self):
        self.queue = []
        self.halfLifeManager = halfLifeManager()


    def add(self, priority: int, action, actionType: actionStatus, speed=1):
        element = (priority, action, actionType, speed)
        if len(self.queue) == 0:
            self.queue.append(element)
        for i, action in enumerate(self.queue):
            if element[0] < action[0]:
                self.queue.insert(i, element)
                return None

        self.queue.append(element)

    def run(self):
        if len(self.queue) == 0:
            return None

        action = self.queue.pop(0)
        if action[2] == actionStatus.SHOOTING:
            self.halfLifeManager.shoot()
        elif action[2] == actionStatus.TURNING:
            self.halfLifeManager.turn(action[1])
        elif action[2] == actionStatus.WALKING:
            self.halfLifeManager.walk(action[1])




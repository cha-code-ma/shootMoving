

class shootDetector():

    def isShooting(self, valuesList, timeList) -> bool:
        accelList, gyroList = valuesList[0:3], valuesList[3:7]

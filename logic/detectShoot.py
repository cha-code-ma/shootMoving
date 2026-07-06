

class shootDetector():

    def isShooting(self, valuesList, timeList) -> bool:
        accelList, gyroList = valuesList[0:3], valuesList[3:7]
        axList = accelList[0]
        ayList = accelList[1]
        axAverage = self.averageInList(axList, 10)
        ayAverage = self.averageInList(ayList, 10)

        if axAverage >= 0.75:
            None

        if ayAverage >= 0.75:
            None


    def averageInList(self, list, startIndex):
        if len(list) <= startIndex:
            startIndex = 0
        if len(list) == 0:
            return 0

        sum = 0
        for i in range(startIndex, len(list)):
            sum += list[i]
        sum = sum/(len(list) - startIndex)

        return sum




class shootDetector():
    ACCEL_TRESHOLD = 0.5
    GRAVITY_TRESHOLD = 0.75


    def isShooting(self, valuesList, timeList) -> tuple[bool, float]:
        accelList, gyroList = valuesList[0:3], valuesList[3:7]
        axList = accelList[0]
        ayList = accelList[1]
        azList = accelList[2]
        axAverage = self.averageInList(axList, 10)
        ayAverage = self.averageInList(ayList, 10)
        azAverage = self.averageInList(azList, 10)
        checks = [(axAverage, [ayList, azList]),
                   (ayAverage, [axList, azList]),
                   (azAverage, [axList, ayList])]

        for av, lists in checks:
            for aList in lists:
                shot, strength = self.fluctuation(aList, timeList, self.ACCEL_TRESHOLD, 10)
                if av >= self.GRAVITY_TRESHOLD and shot:
                    return shot, strength
        return False, 0


    def averageInList(self, list, startIndex):
        if not self.check(list, startIndex):
            return 0

        sum = 0
        for i in range(startIndex, len(list)):
            sum += list[i]
        sum = sum/(len(list) - startIndex)

        return sum

    def fluctuation(self, list, time, treshold, startIndex) -> tuple[bool, float]:
        if not self.check(list, startIndex):
            return False, 0

        pos = False
        neg = False
        highValues = [x for x in list if x >= self.ACCEL_TRESHOLD]
        lowValues = [x for x in list if x <= -self.ACCEL_TRESHOLD]
        if len(highValues) > 1 and len(lowValues) > 1:
            return True, (self.averageInList(highValues, 0) + self.averageInList(lowValues, 0) ) / 2
        return False, 0

    def check(self, list, startIndex) -> bool:
        if len(list) == 0 or len(list) <= startIndex:
            return False
        return True
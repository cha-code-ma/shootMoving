"""

"""
class shootDetector():
    ACCEL_TRESHOLD = 0.5
    GRAVITY_TRESHOLD = 0.75

    def low_varation(self, list, value=0, band=0.3, precantage=0.8):
        inBandList = [x for x in list if -band + value <= x <= band + value]
        x = len(inBandList)/len(list)
        if x >= precantage:
            return True
        return False

    def stopShooting(self, valuesList, timeList, amountSamples = 6) -> bool:
        accelList, gyroList = valuesList[0:3], valuesList[3:7]
        axList = accelList[0][-amountSamples:]
        ayList = accelList[1][-amountSamples:]
        azList = accelList[2][-amountSamples:]
        if not self.check(axList, amountSamples):
            return False
        axAverage = self.averageInList(axList, -amountSamples)
        ayAverage = self.averageInList(ayList, -amountSamples)
        azAverage = self.averageInList(azList, -amountSamples)

        if self.low_varation(axList, axAverage) and \
            self.low_varation(ayList, ayAverage) and \
            self.low_varation(azList, azAverage):
            return True
        return False


    def isShooting(self, valuesList, timeList, amountSamples = 10) -> tuple[bool, float]:

        accelList, gyroList = valuesList[0:3], valuesList[3:7]
        axList = accelList[0][-amountSamples:]
        ayList = accelList[1][-amountSamples:]
        azList = accelList[2][-amountSamples:]
        if not self.check(axList, amountSamples):
            return False, 0
        axAverage = self.averageInList(axList, -amountSamples)
        ayAverage = self.averageInList(ayList, -amountSamples)
        azAverage = self.averageInList(azList, -amountSamples)
        checks = [(axAverage, [ayList, azList]),
                   (ayAverage, [axList, azList]),
                   (azAverage, [axList, ayList])]

        for av, lists in checks:
            for aList in lists:
                shot, strength = self.fluctuation(aList, timeList, self.ACCEL_TRESHOLD, -amountSamples)
                if  shot: #av >= self.GRAVITY_TRESHOLD and
                    return shot, strength
        return False, 0


    def averageInList(self, list, startIndex):
        if not self.check(list, startIndex):
            return 0

        if startIndex < 0:
            startIndex = len(list) + startIndex


        sum = 0
        for i in range(startIndex, len(list)):
            sum += list[i]
        sum = sum/(len(list) - startIndex)

        return sum

    def fluctuation(self, list, time, treshold, startIndex) -> tuple[bool, float]:
        if not self.check(list, startIndex):
            return False, 0

        if startIndex < 0:
            startIndex = len(list) + startIndex

        highValues = [x for x in list[-startIndex:] if x >= self.ACCEL_TRESHOLD]
        lowValues = [x for x in list[-startIndex:] if x <= -self.ACCEL_TRESHOLD]
        if len(highValues) > 1 and len(lowValues) > 1:
            return True, (self.averageInList(highValues, 0) + self.averageInList(lowValues, 0) ) / 2
        return False, 0

    def check(self, list, startIndex) -> bool:
        if len(list) == 0 or len(list) < abs(startIndex):
            return False
        return True

    """
    def logging(self, fallType):

        Logs a fall incident with date, time, max acceleration values and fall type.

        if self._logDebug:
            self._logDebug = not self._logDebug
            self._logDebugTimer = 0
        else:
            return

        amountFramesCheck = min(
            min(len(self.allAccelValues[0]),
                len(self.allAccelValues[1]),
                len(self.allAccelValues[2])),
            1000 // TIMER_INTERVAL_VALUE)

        self._maxAcceleration = [[], [], []]
        for i in range(3):
            maxValue = 0
            for frame in range(1, amountFramesCheck + 1):
                if abs(self.allAccelValues[i][-frame]) > maxValue:
                    maxValue = abs(self.allAccelValues[i][-frame])
            self._maxAcceleration[i].append(maxValue)

        date = datetime.datetime.now().date()
        currentTime = datetime.datetime.now().time()
        dateText = str(date.year).zfill(2) + ":" + str(date.month).zfill(2) + ":" + str(date.day).zfill(2)
        currentTimeText = str(currentTime.hour).zfill(2) + ":" + \
            str(currentTime.minute).zfill(2) + ":" + str(currentTime.second).zfill(2)

        axText = round(self._maxAcceleration[0][0], 3)
        ayText = round(self._maxAcceleration[1][0], 3)
        azText = round(self._maxAcceleration[2][0], 3)

        text = [dateText, currentTimeText, axText, ayText, azText, fallType]
        self._log.append(text)
        self._logModel.appendRow(QStandardItem(
            f"Date:{text[0]} Time:{text[1]} | ax:{text[2]} ay:{text[3]} az:{text[4]} | Falltype: {text[5]}"))
        print(self._log)
        """
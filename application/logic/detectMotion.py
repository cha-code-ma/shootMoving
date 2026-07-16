"""

"""
from logic.enums import turningStatus, walkingStatus, actionStatus
from halfLife.halfLifeShooting import halfLifeManager
from logic.prioqueue import  prioQueue

class movementDetector():
    ACCEL_TRESHOLD = 1.2
    GRAVITY_TRESHOLD = 0.75

    BLOCK_TURN_DURATION = 0.9
    TURNING_TRESHOLD = 100

    WALKING_TRESHOLD = 100
    BLOCK_WALK_DURATION = 0.8
    def __init__(self):
        #shoot variables:
        self.prioQueue = prioQueue()
        self.lastRegisterdShootTime = 0
        self.shooting = False


        #turning variables:
        self.blockedTurningStartTime = 0
        self.turningStatus = turningStatus.STRAIGHT
        self.speedTurning = 1
        self.lastRegisteredTurnTime = 0

        #walking variables:

        self.lastStartWalkingTime = 0
        self.walkingDirection = walkingStatus.STANDING
        self.speedWalking = 1
        self.lastRegisterdWalkTime = 0

        #halfLife:
        self.halfLifeManager = halfLifeManager()

    def walking(self, valuesList, timeList, amountSamples=10):
        currentTime = timeList[-1]
        if not currentTime:
            currentTime = 0
        timeList = timeList[-amountSamples:]
        accelList, gyroList = valuesList[0:3], valuesList[3:7]
        gyList = gyroList[1][-amountSamples:]
        lastActivationIndex, positive, self.lastRegisterdWalkTime = self.mostRecentIndex(timeList, gyList, self.lastRegisterdWalkTime, self.WALKING_TRESHOLD)

        if lastActivationIndex is not None:
            if self.walkingDirection == walkingStatus.STANDING:
                if positive:
                    self.walkingDirection = walkingStatus.FORWARD
                    self.lastStartWalkingTime = currentTime
                    self.prioQueue.add(1, self.walkingDirection ,actionStatus.WALKING)
                    #self.halfLifeManager.walk(self.walkingDirection)
                else:
                    self.walkingDirection = walkingStatus.BACKWARD
                    self.lastStartWalkingTime = currentTime
                    self.prioQueue.add(1, self.walkingDirection ,actionStatus.WALKING)

                    #self.halfLifeManager.walk(self.walkingDirection)

        if currentTime - self.lastStartWalkingTime >= 0.9:
            self.walkingDirection = walkingStatus.STANDING

        return self.walkingDirection



    def low_varation(self, list, value=0, band=0.3, precantage=0.8):
        inBandList = [x for x in list if -band + value <= x <= band + value]
        x = len(inBandList)/len(list)
        if x >= precantage:
            return True
        return False

    def shoot(self, valueList, timeList, amountSamples=2):
        currentTime = timeList[-1]
        shoot, _ = self.isShooting(valueList, timeList)
        shot = not self.stopShooting(valueList, timeList)
        if currentTime - self.lastRegisterdShootTime > 0.2 and shot:
            self.prioQueue.add(2,None ,actionStatus.SHOOTING)
            #self.halfLifeManager.shoot()
            self.lastRegisterdShootTime = currentTime
        return shot

    def stopShooting(self, valuesList, timeList, amountSamples = 2) -> bool:
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
                    if gyroList[2][-1]  < 100:
                        return shot, strength
        return False, 0


    def mostRecentIndex(self, time, valueList, lastRegisteredTime, treshold) -> tuple[int, bool]:
        recentIndex = None
        positive = None
        HighValues = [[x, i] for i, x in enumerate(valueList) if x > treshold]
        lowValues = [[x, i] for i, x in enumerate(valueList) if x < -treshold]

        if len(HighValues) > 0 and len(lowValues) > 0:
            indexHighValues = list(zip(*HighValues))[1]
            recentHighIndex = max(indexHighValues)
            indexLowValues = list(zip(*lowValues))[1]
            recentLowIndex = max(indexLowValues)

            if recentHighIndex > recentLowIndex:
                if time[recentHighIndex] > lastRegisteredTime:
                    recentIndex = recentHighIndex
                    positive = True
                else:
                    recentIndex = None
            else:
                if time[recentLowIndex] > lastRegisteredTime:
                    recentIndex = recentLowIndex
                    positive = False
                else:
                    recentIndex = None

        elif len(lowValues) > 0:
            indexLowValues = list(zip(*lowValues))[1]
            recentLowIndex = max(indexLowValues)
            if time[recentLowIndex] > lastRegisteredTime:
                recentIndex = recentLowIndex
                positive = False
            else:
                recentIndex = None
        elif len(HighValues)  > 0:
            indexHighValues = list(zip(*HighValues))[1]
            recentHighIndex = max(indexHighValues)
            if time[recentHighIndex] > lastRegisteredTime:
                recentIndex = recentHighIndex
                positive = True
            else:
                recentIndex = None
        else:
            recentIndex = None
        return recentIndex, positive, lastRegisteredTime


    def turning(self, valuesList: list, timeList: list, amountSamples=10) -> tuple[turningStatus, bool]:
        """
        if turning == turningStatus.TURNING:
            print(f"turning: {direc}")
            self.halfLifeManager.turn(direc)
        """

        currentTime = timeList[-1]
        if not currentTime:
            currentTime = 0
        timeList = timeList[-amountSamples:]
        accelList, gyroList = valuesList[0:3], valuesList[3:7]
        gzList = gyroList[2][-amountSamples:]
        lastActivationIndex, positive, self.lastRegisteredTurnTime = self.mostRecentIndex(timeList, gzList, self.lastRegisteredTurnTime, self.TURNING_TRESHOLD)

        if lastActivationIndex is not None:
            if self.turningStatus == turningStatus.STRAIGHT:
                if positive:

                    self.turningStatus = turningStatus.LEFT
                    self.lastRegisteredTurnTime = currentTime
                    self.prioQueue.add(1, self.turningStatus, actionStatus.TURNING)
                    #self.halfLifeManager.turn(self.turningStatus)
                else:

                    self.turningStatus = turningStatus.RIGHT
                    self.lastRegisteredTurnTime = currentTime
                    self.prioQueue.add(1, self.turningStatus, actionStatus.TURNING)
                    #self.halfLifeManager.turn(self.turningStatus)

        if currentTime - self.lastRegisteredTurnTime >= 0.9:
            self.turningStatus = turningStatus.STRAIGHT


        return self.turningStatus


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
        average = sum(list[-startIndex:]) / len(list)
        highValues = [x for x in list[-startIndex:] if x >= average + self.ACCEL_TRESHOLD]
        lowValues = [x for x in list[-startIndex:] if x <= average - self.ACCEL_TRESHOLD]
        if len(highValues) > 1 and len(lowValues) > 1:
            return True, (self.averageInList(highValues, 0) + self.averageInList(lowValues, 0) ) / 2
        return False, 0

    def check(self, list, startIndex) -> bool:
        if len(list) == 0 or len(list) < abs(startIndex):
            return False
        return True

    def getStatus(self, allValues, time):
        shot = self.shoot(allValues, time)
        turning = self.turning(allValues, time)
        walking = self.walking(allValues, time)
        self.prioQueue.run()
        return shot, turning, walking



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
"""
def csvSave(self):
with open(self.csv_filename, 'w') as f:
    f.write("t,x,y,z\n")
    for t, ax, ay, az in zip(self.listAllT, self.listAllAx, self.listAllAy, self.listAllAz):
        f.write(f"{round(t, 2)},{round(ax, 2)},{round(ay, 2)},{round(az, 2)}\n")
"""
"""
        #Logging:
        self._log = []
        self._logModel = QStandardItemModel()
        self.ui.logList.setModel(self._logModel)
        self._logDebug = True
        self._logDebugTimer = -1
        self._csv_filename = None
"""
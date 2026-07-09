"""

"""
from enum import Enum


class direction(Enum):
    LEFT = -1
    FORWARD = 0
    RIGHT = 1

class turningStatus(Enum):
    TURNING = 1
    NO_TURNING = 0

class blocking(Enum):
    NO_BLOCK = 1
    BLOCK = 0

class walkingStatus(Enum):
    FORWARD = 1
    STANDING = 0
    BACKWARD = -1

class movementDetector():
    ACCEL_TRESHOLD = 0.8
    GRAVITY_TRESHOLD = 0.75

    BLOCK_TURN_DURATION = 0.9
    TURNING_TRESHOLD = 100

    WALKING_TRESHOLD = 100
    BLOCK_WALK_DURATION = 0.8
    def __init__(self):
        #turning variables:
        self.blockedTurning = blocking.NO_BLOCK
        self.blockedTurningStartTime = 0
        self.angleTurning = direction.FORWARD
        self.turningStatus = turningStatus.NO_TURNING
        self.speedTurning = 1
        self.lastRegisteredTurnTime = 0

        #walking variables:
        self.blockedWalking = blocking.NO_BLOCK
        self.lastRegisterdWalkTime = 0
        self.walkingDirection = walkingStatus.STANDING
        self.speedWalking = 1

    def walking(self, valuesList, timeList, amountSamples=6) -> tuple[walkingStatus, float]:
        currentTime = timeList[-1]
        if not currentTime:
            currentTime = 0

        accelList, gyroList = valuesList[0:3], valuesList[3:7]
        gxList = gyroList[0][-amountSamples:]


        XHighValues = [[x, i] for i, x in enumerate(gxList) if x > self.WALKING_TRESHOLD]
        XlowValues = [[x, i] for i, x in enumerate(gxList) if x < -self.WALKING_TRESHOLD]

        if len(XHighValues) > 0:
            indexHighValues = list(zip(*XHighValues))[1]
            recentHighIndex = max(indexHighValues)
        if len(XlowValues) > 0:
            indexLowValues = list(zip(*XlowValues))[1]
            recentLowIndex = max(indexLowValues)
        if self.blockedTurning == blocking.NO_BLOCK:
            if len(XHighValues) > 0 and len(XlowValues) > 0:
                if recentHighIndex > recentLowIndex:
                    if timeList[-amountSamples:][recentHighIndex] <= self.lastRegisterdWalkTime:# and self.walkingDirection == WalkingStatus.STANDING
                        self.lastRegisterdWalkTime = currentTime
                    else:
                        self.walkingDirection = walkingStatus.FORWARD
                        self.blockedWalking = blocking.BLOCK
                        self.lastRegisterdWalkTime = currentTime
                elif recentLowIndex > recentHighIndex:
                    if timeList[-amountSamples:][recentLowIndex] <= self.lastRegisterdWalkTime:# and self.walkingDirection == WalkingStatus.STANDING
                        self.lastRegisterdWalkTime = currentTime
                    else:
                        self.walkingDirection = walkingStatus.BACKWARD
                        self.blockedWalking = blocking.BLOCK
                        self.lastRegisterdWalkTime = currentTime
            elif len(XHighValues) > 0:
                if timeList[-amountSamples:][recentHighIndex] <= self.lastRegisterdWalkTime:# and self.walkingDirection == WalkingStatus.STANDING
                        self.lastRegisterdWalkTime = currentTime
                else:
                    self.walkingDirection = walkingStatus.FORWARD
                    self.blockedWalking = blocking.BLOCK
                    self.lastRegisterdWalkTime = currentTime
            elif len(XlowValues) > 0:
                if timeList[-amountSamples:][recentLowIndex] <= self.lastRegisterdWalkTime:# and self.walkingDirection == WalkingStatus.STANDING
                        self.lastRegisterdWalkTime = currentTime
                else:
                    self.walkingDirection = walkingStatus.BACKWARD
                    self.blockedWalking = blocking.BLOCK
                    self.lastRegisterdWalkTime = currentTime
            else:
                self.walkingDirection = walkingStatus.STANDING

        else: #block, dus eigenlijk niks, maar update tijd, block
            if currentTime - self.lastRegisterdWalkTime >= self.BLOCK_WALK_DURATION:
                self.blockedWalking = blocking.NO_BLOCK
                self.walkingDirection = walkingStatus.STANDING
            else:
                self.walkingDirection = walkingStatus.STANDING

        return self.walkingDirection, self.speedWalking














    def low_varation(self, list, value=0, band=0.3, precantage=0.8):
        inBandList = [x for x in list if -band + value <= x <= band + value]
        x = len(inBandList)/len(list)
        if x >= precantage:
            return True
        return False

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
                    return shot, strength
        return False, 0

    def turning(self, valuesList: list, timeList: list, amountSamples=10) -> tuple[turningStatus, direction, float]:
        currentTime = timeList[-1]
        if not currentTime:
            currentTime = 0

        accelList, gyroList = valuesList[0:3], valuesList[3:7]
        gzList = gyroList[2][-amountSamples:]

        if self.blockedTurning == blocking.NO_BLOCK:
            ZHighValues = [[x, i] for i, x in enumerate(gzList) if x > self.TURNING_TRESHOLD]
            ZlowValues = [[x, i] for i, x in enumerate(gzList) if x < -self.TURNING_TRESHOLD]

            if len(ZHighValues) > 0:
                indexHighValues = list(zip(*ZHighValues))[1]
                recentHighIndex = max(indexHighValues)
            if len(ZlowValues) > 0:
                indexLowValues = list(zip(*ZlowValues))[1]
                recentLowIndex = max(indexLowValues)

            if len(ZHighValues) > 0 and len(ZlowValues) > 0:
                if recentLowIndex > recentHighIndex:
                    if timeList[-amountSamples:][recentLowIndex] <= self.lastRegisteredTurnTime : #and self.angleTurning == direction.FORWARD
                        self.angleTurning = direction.FORWARD
                        self.turningStatus = turningStatus.NO_TURNING
                    else:
                        self.angleTurning = direction.LEFT
                        self.blockedTurning = blocking.BLOCK
                        self.blockedTurningStartTime = currentTime
                        self.turningStatus = turningStatus.TURNING
                        self.lastRegisteredTurnTime = currentTime
                elif recentHighIndex > recentLowIndex:
                    if timeList[-amountSamples:][recentHighIndex] <= self.lastRegisteredTurnTime:
                        self.angleTurning = direction.FORWARD
                        self.turningStatus = turningStatus.NO_TURNING
                    else:
                        self.angleTurning = direction.RIGHT
                        self.blockedTurningStartTime = currentTime
                        self.blockedTurning = blocking.BLOCK
                        self.turningStatus = turningStatus.TURNING
                        self.lastRegisteredTurnTime = currentTime

            elif len(ZHighValues) > 0:
                if timeList[-amountSamples:][recentHighIndex] <= self.lastRegisteredTurnTime:
                    self.angleTurning = direction.FORWARD
                    self.turningStatus = turningStatus.NO_TURNING
                else:
                    self.angleTurning = direction.RIGHT
                    self.blockedTurning = blocking.BLOCK
                    self.blockedTurningStartTime = currentTime
                    self.turningStatus = turningStatus.TURNING
                    self.lastRegisteredTurnTime = currentTime

            elif len(ZlowValues) > 0:
                if timeList[-amountSamples:][recentLowIndex] <= self.lastRegisteredTurnTime:
                    self.angleTurning = direction.FORWARD
                    self.turningStatus = turningStatus.NO_TURNING
                else:
                    self.angleTurning = direction.LEFT
                    self.blockedTurning = blocking.BLOCK
                    self.blockedTurningStartTime = currentTime
                    self.turningStatus = turningStatus.TURNING
                    self.lastRegisteredTurnTime = currentTime
            else:
                self.angleTurning = direction.FORWARD
                self.turningStatus = turningStatus.NO_TURNING

        else:  # self.blocked == blocking.BLOCK
            tijdVerstreken = currentTime - self.blockedTurningStartTime
            isAtRest = self.is_at_rest(gzList)

            if tijdVerstreken >= self.BLOCK_TURN_DURATION and isAtRest:
                self.blockedTurning = blocking.NO_BLOCK
                self.turningStatus = turningStatus.NO_TURNING
                self.angleTurning = direction.FORWARD
            else:
                # nog steeds geblokkeerd: te snel na de vorige draai, OF gyro nog niet tot rust
                self.turningStatus = turningStatus.NO_TURNING
                self.angleTurning = direction.FORWARD

        return self.turningStatus, self.angleTurning, self.speedTurning

    def is_at_rest(self, gzList, band=None, percentage=0.8):
        """Checkt of de recente gz-waarden grotendeels dicht bij 0 liggen (rustig),
        ongeacht of dat via een terugflik of langzame terugkeer kwam."""
        if band is None:
            band = self.TURNING_TRESHOLD * 0.3
        if len(gzList) == 0:
            return False
        inBand = [x for x in gzList if -band <= x <= band]
        return (len(inBand) / len(gzList)) >= percentage


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
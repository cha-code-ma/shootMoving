"""
Gemaakt door: Github: cha-code-ma

"""
"""
Notities voor github pushing:

dit is de start, geen implementatie, alleen basis voor PyQt5

"""

import logic.detectArduino, logic.detectShoot
from GUI.window_ui import Ui_Form
from halfLife.halfLifeShooting import halfLifeManager
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from .mplwidget import MplWidget
from .window_ui import *
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
TIMER_INTERVAL_VALUE = 200
AMOUNT_OF_ARDUINO_VALUES = 7
AMOUNT_OF_MOMENTS = 100
AMOUNT_OF_GRAPH_MOMENTS = 30
ARDUINO_LOCAL_NAME = "BLE-AR48"  #Use the correct Arduino number in this identifier!!
LED_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
on_value = bytearray([0x01])
off_value = bytearray([0x00])

class shootMovingUI(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)

        #All variables:
        self.allValues = [[0] for i in range(AMOUNT_OF_ARDUINO_VALUES - 1)]
        #self.varList = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
        self.time = [0]
        self.graphValues = [[0] for i in range(AMOUNT_OF_ARDUINO_VALUES - 1)]

        #MPLwidget:
        self.ui = Ui_Form()
        self.timer = QTimer()
        self.timer.setInterval(TIMER_INTERVAL_VALUE)
        self.timer.timeout.connect(self.timerEvent)
        self.ui.setupUi(self)
        self.setWindowTitle("Project")
        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.legend()
        self.ui.MplWidget.canvas.draw()

        #UI initialisation:
        """
        At the start, all buttons need to be hid, except
        buttonChoose....
        """
        self.ui.buttonTest.hide()
        self.ui.MplWidget.hide()
        self.ui.groupBoxSimu.hide()

        #UI logic:
        self.ui.buttonChooseStart.clicked.connect(self.demonstrationFunction)
        self.ui.buttonChooseTest.clicked.connect(self.demonstrationFunction)

        #Logging:
        self._log = []
        self._logModel = QStandardItemModel()
        self.ui.logList.setModel(self._logModel)
        self._logDebug = True
        self._logDebugTimer = -1
        self._csv_filename = None

        #BLE communication:
        self.bleComManager = logic.detectArduino.BleCommunicationManager()
        self.bleComManager.data.connect(self.addValues)
        self.ui.buttonTest.clicked.connect(self.startFunction)

        #Shoot Detection:
        self.shootdetector = logic.detectShoot.shootDetector()
        self.isShooting = False

        #HalfLife:
        self.halfLifeManager = halfLifeManager()


    def startFunction(self):
        self.bleComManager.start() # .start() start de thread, roept run() aan
        self.timerEvent()
        self.timer.start()

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

    def demonstrationFunction(self):
        """
        laat alle componenten zien.
        """
        self.ui.buttonTest.show()
        self.ui.MplWidget.show()
        self.ui.groupBoxSimu.show()
        self.ui.buttonChooseStart.hide()
        self.ui.buttonChooseTest.hide()

    def shootDetected(self):
        shot, accel = self.shootdetector.isShooting(self.allValues, self.time)
        shot = not self.shootdetector.stopShooting(self.allValues, self.time, 4)

        if shot:
            self.isShooting = True
            self.ui.shootDetectionText.setPlainText(f"Is shooting: {accel}")
            self.ui.shootDetectionText.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            self.isShooting = False
            self.ui.shootDetectionText.setPlainText(f"Is NOT shooting")
            self.ui.shootDetectionText.setStyleSheet("background-color: rgb(255, 0, 0);")

    def startButtonClicked(self):
            self.timer.start()

    def csvSave(self):
        with open(self.csv_filename, 'w') as f:
            f.write("t,x,y,z\n")
            for t, ax, ay, az in zip(self.listAllT, self.listAllAx, self.listAllAy, self.listAllAz):
                f.write(f"{round(t, 2)},{round(ax, 2)},{round(ay, 2)},{round(az, 2)}\n")


    def timerEvent(self):

        if self.allValues == [[0], [0], [0], [0], [0], [0]]:
            self.isShooting = False
            self.ui.shootDetectionText.setPlainText(f"Is NOT shooting")
            self.ui.shootDetectionText.setStyleSheet("background-color: rgb(255, 0, 0);")
            return None

        self.shootDetected()
        if self.isShooting:
            self.halfLifeManager.shoot()
        #lastValues = self.chooseValuesIndex(-1)

        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.set_ylim(-4, 4)
        self.ui.MplWidget.canvas.axes.plot(self.time, self.graphValues[0],'r',linewidth= 0.5, label = 'ax')
        self.ui.MplWidget.canvas.axes.plot(self.time, self.graphValues[1],'g',linewidth= 0.5, label = 'ay')
        self.ui.MplWidget.canvas.axes.plot(self.time, self.graphValues[2],'b',linewidth= 0.5, label = 'az')
        self.ui.MplWidget.canvas.axes.set_xlabel("tijd (s)")
        self.ui.MplWidget.canvas.axes.set_ylabel("acceleration (9,81 m/s^2)")
        self.ui.MplWidget.canvas.axes.figure.tight_layout()
        self.ui.MplWidget.canvas.axes.legend(loc= 'upper left')
        self.ui.MplWidget.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    form = shootMovingUI()
    form.show()
    sys.exit(app.exec_())
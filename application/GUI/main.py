"""
Gemaakt door: Github: cha-code-ma

"""
"""
Notities voor github pushing:

dit is de start, geen implementatie, alleen basis voor PyQt5

"""

import logic.detectArduino, logic.detectMotion
from logic.enums import turningStatus, walkingStatus, AMOUNT_OF_CHECKS
from GUI.window_ui import Ui_Form
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
TIMER_INTERVAL_VALUE = 300
AMOUNT_OF_ARDUINO_VALUES = 7
AMOUNT_OF_MOMENTS = 100
AMOUNT_OF_GRAPH_MOMENTS = 30



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
        self.timer.setInterval(1/AMOUNT_OF_CHECKS)
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

        #BLE communication:
        self.bleComManager = logic.detectArduino.BleCommunicationManager()
        self.bleComManager.data.connect(self.addValues)
        self.ui.buttonTest.clicked.connect(self.startFunction)

        #Shoot Detection:
        self.movementDetector = logic.detectMotion.movementDetector()
        self.isShooting = False



    def startFunction(self):
        self.bleComManager.start() # .start() start de thread, roept run() aan
        self.timerEvent()
        self.timer.start()

    def addValues(self, values):
        if type(values) is bool or len(values) != AMOUNT_OF_ARDUINO_VALUES:
            return None
        lastValues = list(zip(*self.allValues))[-1][0:6]
        temp = []
        for i in range(AMOUNT_OF_ARDUINO_VALUES) - 1:
            temp.append(round(values[i], 3))

        if lastValues == temp: # if values are the same as reading before.
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

    def movementDetected(self):

        shot, turning, walking = self.movementDetector.getStatus(self.allValues, self.time)
        if shot:
            self.isShooting = True
            self.ui.shootDetectionText.setPlainText(f"Is shooting: ")
            self.ui.shootDetectionText.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            self.isShooting = False
            self.ui.shootDetectionText.setPlainText(f"Is NOT shooting")
            self.ui.shootDetectionText.setStyleSheet("background-color: rgb(255, 0, 0);")

        if turning == turningStatus.STRAIGHT:
            self.ui.turnDetectionText.setPlainText(f"Is NOT turning")
            self.ui.turnDetectionText.setStyleSheet("background-color: rgb(255, 0, 0);")
        else:
            self.ui.turnDetectionText.setPlainText(f"Is turning: {turning}")
            self.ui.turnDetectionText.setStyleSheet("background-color: rgb(0, 255, 0);")

        if walking == walkingStatus.STANDING:
            self.ui.walkDetextionText.setPlainText(f"Is NOT walking")
            self.ui.walkDetextionText.setStyleSheet("background-color: rgb(255, 0, 0);")
        else:
            self.ui.walkDetextionText.setPlainText(f"Is walking: {walking}")
            self.ui.walkDetextionText.setStyleSheet("background-color: rgb(0, 255, 0);")

    def startButtonClicked(self):
            self.timer.start()

    def timerEvent(self):

        if self.allValues == [[0], [0], [0], [0], [0], [0]]:
            self.isShooting = False
            self.ui.shootDetectionText.setPlainText(f"Is NOT shooting")
            self.ui.shootDetectionText.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.ui.turnDetectionText.setPlainText(f"Is NOT turning")
            self.ui.turnDetectionText.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.ui.walkDetextionText.setPlainText(f"Is NOT walking")
            self.ui.walkDetextionText.setStyleSheet("background-color: rgb(255, 0, 0);")
            return None

        print(f"ax:{self.allValues[0][-1]}   gx:{self.allValues[3][-1]}    gz:{self.allValues[5][-1]}")
        self.movementDetected()


        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.set_ylim(-50, 50)
        self.ui.MplWidget.canvas.axes.plot(self.time, self.graphValues[0],'r',linewidth= 0.5, label = 'ax')
        self.ui.MplWidget.canvas.axes.plot(self.time, self.graphValues[1],'g',linewidth= 0.5, label = 'ay')
        self.ui.MplWidget.canvas.axes.plot(self.time, self.graphValues[2],'b',linewidth= 0.5, label = 'az')
        self.ui.MplWidget.canvas.axes.plot(self.time, self.graphValues[3],'r',linewidth= 0.5, label = 'gx', linestyle = '--')
        self.ui.MplWidget.canvas.axes.plot(self.time, self.graphValues[4],'g',linewidth= 0.5, label = 'gy', linestyle = '--')
        self.ui.MplWidget.canvas.axes.plot(self.time, self.graphValues[5],'b',linewidth= 0.5, label = 'gz', linestyle = '--')
        self.ui.MplWidget.canvas.axes.set_xlabel("tijd (s)")
        self.ui.MplWidget.canvas.axes.set_ylabel("acceleration (9,81 m/s^2)")
        self.ui.MplWidget.canvas.axes.figure.tight_layout()
        self.ui.MplWidget.canvas.axes.legend(loc='upper left')
        self.ui.MplWidget.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    form = shootMovingUI()
    form.show()
    sys.exit(app.exec_())
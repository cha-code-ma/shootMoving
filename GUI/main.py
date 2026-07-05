"""
Gemaakt door: Github: cha-code-ma

"""
"""
Notities voor github pushing:

dit is de start, geen implementatie, alleen basis voor PyQt5

"""
import argparse
import asyncio
from bleak import BleakClient
from bleak import BleakScanner

import logic.detectArduino
from GUI.window_ui import Ui_Form
import sys
import datetime
import os
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import random
from .mplwidget import MplWidget
from statistics import mean, stdev
from window_ui import *
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
TIMER_INTERVAL_VALUE = 100
ARDUINO_LOCAL_NAME = "BLE-AR48"  #Use the correct Arduino number in this identifier!!
LED_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
on_value = bytearray([0x01])
off_value = bytearray([0x00])

class shootMovingUI(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)

        #All variables:
        self.allValues = [[0], [0], [0], [0], [0], [0]]
        #self.varList = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']

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


    def startFunction(self):
        self.bleComManager.start() # .start() start de thread, roept run() aan
        self.timerEvent()
        self.timer.start()

    def addValues(self, values):
        if type(values) is bool or len(values) != 6:
            return None

        for i in range(6):
            self.allValues[i].append(values[i])

        if len(self.allValues[0]) > 100:
            for i in range(len(self.allValues)):
                self.allValues[i].pop(0)

    def chooseValuesIndex(self, index):
        list = []
        for i in range(6):
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



    def startButtonClicked(self):
            self.timer.start()

    def csvSave(self):
        with open(self.csv_filename, 'w') as f:
            f.write("t,x,y,z\n")
            for t, ax, ay, az in zip(self.listAllT, self.listAllAx, self.listAllAy, self.listAllAz):
                f.write(f"{round(t, 2)},{round(ax, 2)},{round(ay, 2)},{round(az, 2)}\n")


    def timerEvent(self):

        lastValues = self.chooseValuesIndex(-1)
        print(f"lastValues:\n{lastValues}")
        self.ui.MplWidget.canvas.axes.clear()
        #self.ui.MplWidget.canvas.axes.set_ylim( , )
        #self.ui.MplWidget.canvas.axes.plot(self.t, self.list_ax,'r',linewidth= 0.5, label = 'x')
        #self.ui.MplWidget.canvas.axes.plot(self.t, self.list_ay,'g',linewidth= 0.5, label = 'y')
        #self.ui.MplWidget.canvas.axes.plot(self.t, self.list_az,'b',linewidth= 0.5, label = 'z')
        #self.ui.MplWidget.canvas.axes.set_xlabel("tijd (s)")
        #self.ui.MplWidget.canvas.axes.set_ylabel("acceleration (9,81 m/s^2)")
        #self.ui.MplWidget.canvas.axes.figure.tight_layout()
        #self.ui.MplWidget.canvas.axes.legend(loc= 'upper left')
        #self.ui.MplWidget.canvas.draw()

    def logging(self, fallType):
        """
        Logs a fall incident with date, time, max acceleration values and fall type.
        """
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


if __name__ == "__main__":
    app = QApplication([])
    form = shootMovingUI()
    form.show()
    sys.exit(app.exec_())
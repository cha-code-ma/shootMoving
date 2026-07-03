"""
Gemaakt door: Github: cha-code-ma

"""
"""
Notities voor github pushing:

dit is de start, geen implementatie, alleen basis voor PyQt5

"""


import sys

import time
import os
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import random
from statistics import mean, stdev
from project_ui import *
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

TIMER_INTERVAL_VALUE = 100

class Lab1(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)

        #All variables:
        self._ax = 0
        self._ay = 0 #accelerometer x,y,z
        self._az = 0

        self._gx = 0
        self._gy = 0 #gyroscoop x,y,z
        self._gz = 0

        self.t = [] #time

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
        """
        Dit is van lab2.
        """
        with open(self.csv_filename, 'w') as f:
            f.write("t,x,y,z\n")
            for t, ax, ay, az in zip(self.listAllT, self.listAllAx, self.listAllAy, self.listAllAz):
                f.write(f"{round(t, 2)},{round(ax, 2)},{round(ay, 2)},{round(az, 2)}\n")


    def timerEvent(self):


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


    # a = accelerometer
    @property
    def ax(self):
        return self._ax

    @ax.setter
    def ax(self,value):
        self._ax = value


    @property
    def ay(self):
        return self._ay

    @ay.setter
    def ay(self,value):
        self._ay = value


    @property
    def az(self):
        return self._az

    @az.setter
    def az(self,value):
        self._az = value



    # g = gyroscoop
    @property
    def gx(self):
        return self._gx

    @gx.setter
    def gx(self,value):
        self._gx = value


    @property
    def gy(self):
        return self._gy

    @gy.setter
    def gy(self,value):
        self._gy = value


    @property
    def gz(self):
        return self._gz

    @gz.setter
    def gz(self,value):
        self._gz = value

if __name__ == "__main__":
    app = QApplication([])
    form = Lab1()
    form.show()
    sys.exit(app.exec_())
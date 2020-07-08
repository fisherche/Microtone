import sounddevice
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import guitarTuner
import numpy as np 
import time
import sys

class TunerApp(QMainWindow):
    """
    A TunerApp has a fretboard
                    A fretboard has frets
    """
    def __init__(self,*args, **kwargs):
        super(TunerApp, self).__init__(*args, **kwargs)
        #self.app = QApplication(sys.argv)
        self.title = 'Microtonal Guitar Tuner'
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 400
        self.layout = QVBoxLayout()
        #self.setLayout(self.layout)
        self.fretboard = guitarTuner.Fretboard(6, 25)
        self.layout.addLayout(self.fretboard)
        
        self.initializeUI()
        self.initializeFretboardUI()
        self.show()
        
    def initializeUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.initializeFretboardUI()
        
        #add widgets to the layout

    def initializeFretboardUI(self):
        #TODO left-handed option
        #TODO I assume I need to add button/label widgets to the layout this way    

        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tuner = TunerApp()
    sys.exit(app.exec_())
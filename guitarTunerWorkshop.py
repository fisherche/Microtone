import sounddevice
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import guitarTuner
import numpy as np 
import time

class TunerApp(QDialog):

    def __init__(self,**kwargs):
        super(TunerApp, self).__init__(**kwargs)
        self.app = QApplication(sys.argv)
        self.title = 'Microtonal Guitar Tuner'
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 400

        self.fretboard = guitarTuner.Fretboard(6, 25, 12)

        self.initializeUI()
        sys.exit(self.app.exec_())

    
    def initializeUI(self):
        """
        Initializes UI of 
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initializeFretboardUI()
        layout = QGridLayout()
        #add widgets to the layout

    def initializeFretboardUI(self):
        #TODO I assume I need to add button/label widgets to the layout this way
        

        if __name__ == '__main__':
            app = TunerApp(sys.argv)
            
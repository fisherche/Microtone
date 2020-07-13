from audioDevice import AudioDevice
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QMainWindow, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize

import numpy as np 
import time
import sys
    
class ED2Instrument():
    def __init__(self,numberOfStrings):
        self.ed2 = None
        self.referenceHz = None
        self.resonator = AudioDevice()
        self.openNotes = [0]*numberOfStrings #List that stores open string note indices

        self.strings = [] #List that stores lists of playable notes

    #returns a list of frequency values
    def generateAssignED2(self, nEDO, referenceHz=440, lowestHz=20, highestHz = 3000):
        """
        calculates frequency values"""
        #calculate which key the reference is
        key = 0
        if referenceHz < lowestHz:
            print("Reference Hz lower than lowest allowable")
            return
        if referenceHz > highestHz:
            print("Reference Hz higher than highest allowable")
            return

        currentHz = referenceHz * (2 ** (1 / nEDO))
        ed2List = []
        keyExponent = 0
        while currentHz > lowestHz:
            currentHz = referenceHz * (2 ** (1 / nEDO )) ** (keyExponent)
            ed2List = [currentHz] + ed2List 
            keyExponent -= 1
        highHz = referenceHz*(2**(1/nEDO)) 
        referenceNoteNo = -1 * keyExponent
        keyExponent = 0
        while highHz < highestHz:
            keyExponent += 1
            highHz = referenceHz*(2 ** (1/  nEDO))**(keyExponent)
            ed2List = ed2List + [highHz]
        self.ed2 = ed2List
        self.referenceNoteNo = referenceNoteNo
        self.referenceHz = referenceHz
        return ed2List,referenceNoteNo
    
    def generateCentsED2(self, nEDO):
        centsPerOctave = 1200 #equally divide octave
        centsPerStep = centsPerOctave / nEDO
        return centsPerStep

    def pluckString(self,stringIndex,noteIndex=None):
        if noteIndex is None:
            #assume open Note
            self.resonator.makeAudible(self.openNotes[stringIndex])
        else:
            self.resonator.makeAudible(self.strings[stringIndex][noteIndex])
        return 

    def pluckAllOpenStrings(self,duration=2):
        for i in range(len(self.openNotes)):
            self.resonator.makeAudible(self.ed2[self.openNotes[i]],duration)
            #time.sleep(duration)
        return
    def playED2(self,duration=0.125):
        for i in range(len(self.ed2)):
            self.resonator.makeAudible(self.ed2[i],duration)
    def setAllStrings(self,notes):
        #notes is list of indices
        #will resize openNotes
        self.openNotes = notes

    def tuneHigher(self,stringIndex,checkRange=False):
        if stringIndex >= len(self.openNotes):
            print("string Index out of range")
            return
        if self.ed2 is None:
            print("No ED2 assigned")
        self.openNotes[stringIndex] = (self.openNotes[stringIndex] + 1) % len(self.ed2)
        #TODO utility method for listing frets?
        return
    
    def tuneLower(self,stringIndex,checkRange=False):
        #TODO raise exception?
        if stringIndex >= len(self.strings):
            print("string Index out of range")
            return
        if self.ed2 is None:
            print("No ED2 assigned")
        self.openNotes[stringIndex] = (self.openNotes[stringIndex] - 1) % len(self.ed2)
        return

    def generateFretboard(self,numberOfStrings):
        pass
        #TODO

class ED:
    """
    holds cent values and frequency rep. of an n-Equal Division of the Octave
    I believe this'd be the place to generate/store closest Just Intonation ratios
    An n-EDO is a subset of all n*i-EDOs, where i is an integer
    """

    def __init__(self, nEDO):
        self.nEDO = nEDO
        self.centsPerStep = self.centsPerStep()
        self.centsList = self.generateCentsList() #default note names
        self.noteNames = [self.centsList[i] for i in range(len(self.centsList))]
        #TODO integrateGenerateAssignED2 from guitarTuner.py 

    def centsPerStep(self):
        centsPerOctave = 1200
        return centsPerOctave / self.nEDO

    def generateCentsList(self):
        """
        of form [0, ..., 1200]
        """
        centsList = [i * self.centsPerStep for i in range(0,self.nEDO + 1)]
        self.centsList = centsList
        return centsList
    
    def renameNote(self, index, name):
        self.noteNames[index] = name

class Fret(QPushButton):
    #Frets are used for labelling with scale number, ED2 number, etc, updated by the parent Monochord
    #necessary for clicking and displaying on the screen
    #TODO should each fret HAVE an object
    #TODO inheritance from QWidget
    def __init__(self, parentMonochord, fretNumber, indexED2=None, octaveMultiplier=1):
        """
        A Fret is a QWidget
        A Fret is managed by its parentMonochord
        We can use the fretNumber for tablature 
        """
        super(Fret,self).__init__()
        self.parent = parentMonochord
        self.fretNumber = fretNumber
        self.indexED2 = indexED2 #TODO: redundant? perhaps the parent should manage this
        self.octaveMultiplier = octaveMultiplier
        self.setStyleSheet("background-color:#abdfea")
        self.setMinimumSize(18,18)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setText(str(fretNumber))
        self.setCheckable(True)
        self.stateChanged.connect(self.clicked)
    
    def clicked(self, event):
        """propagate message to parent"""
        if event == 2:
            self.parentMonochord.addToChecked(self)
            self.setStyleClickedOn()
        else:
            self.parentMonochord.removeFromChecked(self)
            self.setStyleClickedOff()
    def setStyleClickedOff(self):
        raise NotImplementedError
    def setStyleClickedOn(self):
        raise NotImplementedError
    
    def displayPitchClass(self):      
        #TODO
        raise NotImplementedError

    def displayED2Index(self):
        self.setText(str(self.indexED2))

    def displayNoteName(self):
        """
        parent maintains the note names
        """
        self.setText(self.parent.EDO.noteNames[self.indexED2])
    
    def displayHz(self):
        #TODO
        raise NotImplementedError

    def setIndex(self,indexED2):
        self.indexED2 = indexED2
        return
    
    def highlightNote(self,color):
        #TODO
        raise NotImplementedError

class Monochord(QHBoxLayout):
    """
    """
    #TODO fret indexing when first element is the 'tuning peg'
    #TODO incorporate AudioDevice from guitarTuner
    #TODO should inherit from Layout and not a widget?
    #since each cord plays at most one note at a time, it makes sense for each to have its own AudioDevice object
    #but this does not generalize to any 2D keyboard--at this time I believe that's okay
    # |<tuning interface>|fret0|fret1|...|fret(n-1)|
    def __init__(self, numberFrets=25, secondHarmonicFret=12, edMultiplier=1, frequency=440):
        super(Monochord,self).__init__()
        self.secondHarmonicFret= secondHarmonicFret
        self.frequency = frequency
        self.numberFrets = 25
        self.frets = [Fret(self,i) for i in range(numberFrets)]#todo add widget
        self.checked = set()
        for fret in self.frets:
            self.addWidget(fret)
        self.EDO = ED(secondHarmonicFret*edMultiplier)
        return

    def addToChecked(self, fret):
        self.checked.add(fret)
        return

    def removeFromChecked(self, fret):
        if i in self.checked:
            self.checked.remove(fret)
        return
    
    def tune(self, ED2index=None, multiplier=None, frequency=440):
        """
        PARAMETERS: ED2index, optional       
        """
        self.frequency = frequency

    def updateFrets(self):
        #TODO
        raise NotImplementedError

    def initializeUI(self):
        #TODO
        raise NotImplementedError
    def 
class Fretboard(QVBoxLayout):
    #Fretboard <- ordered set of Monochords, each of which may divide a different ed2
    #TODO calculate and generate ED2 for collection of monochords
    """
    [lowestString, ... , highestString], so display in reverse order
    """
    def __init__(self, numberOfMonochords=6, numberFrets=25):
        """
        self.monochords stores fretboard labels as pair (index in nEDO, multiplier)
        A Fretboard object has numberOfMonochords Monochords to be tuned independently
            A Monochord has numberFrets Frets
        """
        super(Fretboard, self).__init__()
        self.monochords = [] #collection of Monochord objects
        for string in range(numberOfMonochords):
            monochord = Monochord(numberFrets)
            self.addLayout(monochord)
            self.monochords += [monochord]
    def getMonochord(self, index):
        return self.monochords[index]

    def intonateAllMonochords(self, secondHarmonicFret):
        for monochord in self.monochords:
            monochord.secondHarmonicFret = secondHarmonicFret
        
class GuitarTunerApp:
    def __init__(self,xPos=0, yPos=0, width=400, height=400):
        self.app = QApplication(sys.argv)
        self.dimensions = (width, height)
        self.mainWindow = QMainWindow()
        self.mainWindow.setGeometry(xPos, yPos, self.dimensions[0], self.dimensions[1])
        self.mainWindow.setWindowTitle("Microtonal Guitar Tuner")
        self.mainWindow.show()
        self.layout = Fretboard()
        self.fretboardPlaceholder = QWidget()
        self.fretboardPlaceholder.setLayout(self.layout)
        self.mainWindow.setCentralWidget(self.fretboardPlaceholder)
        self.mainWindow.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    # ad = AudioDevice()
    # ad.makeAudible(340)
    guitar = ED2Instrument(6)
    print(guitar.generateAssignED2(22))
    guitar.setAllStrings([50,59,68,77,86,95])
    for i in range(len(guitar.openNotes)):
        print(guitar.ed2[guitar.openNotes[i]])

    #app = QApplication(sys.argv)
    tuner = GuitarTunerApp()
    #sys.exit(app.exec_())
    
    #guitar.pluckAllOpenStrings()
    #guitar.playED2()


    assert ED(12).generateCentsList() == [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]


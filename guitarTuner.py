from audioDevice import AudioDevice
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import numpy as np 
import time
    
class ED2Instrument():
    def __init__(self,numberOfStrings):
        self.ed2 = None
        self.referenceHz = None
        self.resonator = AudioDevice()
        self.openNotes = [0]*numberOfStrings #List that stores open string note indices

        self.strings = [] #List that stores lists of playable notes


    #returns a list of frequency values
    def generateAssignED2(self, nEDO, referenceHz=440, lowestHz=20, highestHz = 3000):
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
        #TODO raise exception?
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
    #holds cent values and frequency rep. of an n-Equal Division of the Octave
    def __init__(self, nEDO):
        pass
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
        centsList = [i * self.centsPerStep for i in range(0,nEDO + 1)]
        self.centsList = centsList
        return centsList
    
    def renameNote(self, index, name):
        self.noteNames[index] = name

class Fret(QWidget):
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
        self.parent = parentMonochord
        self.fretNumber = fretNumber
        self.indexED2 = indexED2 #TODO: redundant? perhaps the parent should manage this
        self.octaveMultiplier = octaveMultiplier

    def initializeUI(self):
        #TODO
        raise NotImplementedError

    def displayPitchClass(self):      
        #TODO
        raise NotImplementedError

    def displayED2Index(self):
        self.setIconText(str(self.indexED2))

    def displayNoteName(self):
        """
        parent maintains the note names
        """
        self.setIconText(self.parent.EDO.noteNames[self.indexED2])
    
    def displayHz(self):
        #TODO
        raise NotImplementedError

    def setIndex(self,indexED2):
        self.indexED2 = indexED2
        return
    
    def highlightNote(self,color):
        #TODO
        raise NotImplementedError

class Monochord():
    """

    """
    #TODO refactor to no?O9[[uypt be kivy dependent
    #TODO: has- or is a layout?
    #TODO fret indexing when first element is the 'tuning peg'
    #TODO incorporate AudioDevice from guitarTuner
    #TODO should inherit from Layout and not a widget?
    #since each cord plays at most one note at a time, it makes sense for each to have its own AudioDevice object
    #but this does not generalize to any 2D keyboard--at this time I believe that's okay
    # |<tuning interface>|fret0|fret1|...|fret(n-1)|
    def __init__(self, numberFrets=25, secondHarmonicFret=12, frequency=440):
        self.secondHarmonicFret= secondHarmonicFret
        self.frequency = frequency
        self.numberFrets = 25
        self.frets = [Fret(self,i) for i in range(numberFrets)]#todo add widget
        self.drawFrets()
        self.rootIndex = rootIndex
        self.EDO = ED(2,secondHarmonicFret)
        self.layout = GridLayout(rows=1,cols=self.numberFrets,row_force_default=True)

    
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
    


class MainScreen():
    
    def __init__(self,**kwargs):
       
        self.cols = 5
        self.add_widget(Label(text="Microtonal n-EDO Guitar Tuner"))
        self.strings= [] #a list strings of a list strings[i] of button objects associated [downButton,upButton] with the i'th string
        self.open_notes = []
        self.tuner_col = 0 #reference for position calculation

        
        self.tuning_peg_x_offset = 0
        self.prev_tuning_peg_y_offset = 0

        self.tuning_button_scalar = 0.125
        self.tuning_button_x_offset = 5
        self.tuning_button_y_offset = 5
        
        self.open_note_display_size_hint = 0.125
        self.open_note_display_x_offset = 5
        #TODO 1 maintain to ED2 instrument

    def add_string_and_its_widgets(self,start_scale_number=0):
        #TODO update tuner??
        #TODO 2 update reference to ED2 instrument's openNotes
        #TODO use self.size to adjust offsets
        down_button = Button(
            text='Down',
            size_hint=(self.tuning_button_scalar,self.tuning_button_scalar),
            pos = (self.tuning_peg_x_offset, self.prev_tuning_peg_y_offset)
            )

        open_note_display = Label(
            #text=str()
        )
        up_button = Button(
            text='Up',
            size_hint=(self.tuning_button_scalar,self.tuning_button_scalar),
            pos = (self.tuning_peg_x_offset + self.open_note_display_x_offset, self.prev_tuning_peg_y_offset)
            )
        #update y offset

        self.strings += [[down_button,up_button]]
        #update openNotes

    def buildSquareLatticeDisplay(self):
        pass#TODO
    
class SquareLatticeDisplay():
    def __init__(self,buttonMatrix):
        self.built = False
        self.matrix = buttonMatrix
        layout = GridLayout(rows=len(self.matrix),cols=len(self.matrix[0]))

        #TODO: finish display layout
    def build(self):
        self.built = True
        self.root = MainScreen()
        return MainScreen()

class Fretboard:
    #TODO: does this need a scale?
    #Fretboard <- ordered set of Monochords, each of which may divide a different ed2
    #TODO calculate and generate ED2 for collection of monochords
    def __init__(self, numberOfMonochords=6, numberFrets=25):
        """
        self.monochords stores fretboard labels as pair (index in nEDO, multiplier)
        A Fretboard object has numberOfMonochords Monochords to be tuned independently
            A Monochord has numberFrets Frets
        
        """

        self.monochords = [] #collection of Monochord objects
        
        for string in range(numberOfMonochords):
            self.monochords += Monochord(numberFrets)
            for fret in range(numberFrets):
                #make a child button for each one
                #set the label to index in a scale
                #self.monochords[string][fret] = 

                pass
            #make a 
        def getMonochord(self, index):
            return self.monochords[index]


        
        

    def intonateAllMonochords(self, secondHarmonicFret):
        for monochord in self.monochords:
            self.secondHarmonicFret = secondHarmonicFret
        
class GuitarTunerApp:
    def __init__(self,xPos=0, yPos=0, width=400, height=400):
        self.app = QApplication(sys.argv)
        self.dimensions = (width, height)
        self.mainWindow = QMainWindow()
        self.mainWindow.setGeometry(xPos, yPos, dimensions[0], dimensions[1])
        self.mainWindow.setWindowTitle("Microtonal Guitar Tuner")
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
    guitar.pluckAllOpenStrings()
    #guitar.playED2()


    assert ED(12).generateCentsList() == [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]


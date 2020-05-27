from kivy.app import App
from kivy.uix.label import Label 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.event import EventDispatcher
import kivy 
import launchpadLayout

kivy.require('1.11.0')

class Fret:
    #Frets are ordered by index in Monocord
    #Frets are used for labelling with scale number, ED2 number, etc, updated by the parent Monocord
    def __init__(self, )

class Monocord:
    def __init__(self, numberFrets=25, secondHarmonicFret=12):
        self.secondHarmonicFret= secondHarmonicFret
        self.numberFrets = 25
        self.frets = [Fret() for _ in range(numberFrets)]
        for fret in self.frets:




class MainScreen(FloatLayout):
    
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(**kwargs)
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
    
class SquareLatticeDisplay(App):
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
    #Fretboard <- ordered set of Monocords, each of which may divide a different ed2
    #TODO calculate and generate ED2 for collection of monochords
    def __init__(self, numberStrings=6, numberFrets=25:
        """
        self.boardBackend stores fretboard labels as pair (index in nEDO, multiplier)

        """

        self.boardBackend = [] #collection of Monochord objects
        
        for string in range(numberStrings):
            self.boardBackend += 
            for fret in range(numberFrets):
                #make a child button for each one
                #set the label to index in a scale
                #self.boardBackend[string][fret] = 

                pass 
            #make a 
    def intonateAllMonocords(self, secondHarmonicFret):
        for monochord in self.boardBackend:
            self.secondHarmonicFret = secondHarmonicFret
class GuitarTunerApp(App):
    def __init__(self):
        self.built = False
        pass
    def build(self):
        self.built = True
        self.root = MainScreen()
        return MainScreen()
    

class CustomDispatcher(EventDispatcher):
    def __init__(self,**kwargs):
        self.register_event_type('on_test')
        super(CustomDispatcher,self).__init__(**kwargs)
    
    def do_something(self,val):
        self.dispatch('')

if __name__ == '__main__':
    gt = SquareLatticeDisplay(LaunchpadLayout(LaunchpadLayout.scanIO()))
    gt.build()
    gt.run()

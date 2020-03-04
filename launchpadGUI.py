from kivy.app import App
from kivy.uix.label import Label 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.event import EventDispatcher
import kivy 

kivy.require('1.11.0')


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

        self.tuning_button_size_hint = 0.125
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
            size_hint=(self.tuning_button_size_hint,self.tuning_button_size_hint),
            pos = (self.tuning_peg_x_offset, self.prev_tuning_peg_y_offset)
            )

        open_note_display = Label(
            #text=str()
        )
        up_button = Button(
            text='Up',
            size_hint=(self.tuning_button_size_hint,self.tuning_button_size_hint),
            pos = (self.tuning_peg_x_offset + self.open_note_display_x_offset, self.prev_tuning_peg_y_offset)
            )
        #update y offset

        self.strings += [[down_button,up_button]]
        #update openNotes




class GuitarTunerApp(App):
    def __init__(self):
        self.built = False
        pass
    def build(self):
        self.built = True
        return MainScreen()
    

class CustomDispatcher(EventDispatcher):
    def __init__(self,**kwargs):
        self.register_event_type('on_test')
        super(CustomDispatcher,self).__init__(**kwargs)
    
    def do_something(self,val):
        self.dispatch('')

if __name__ == '__main__':
    gt = GuitarTunerApp()

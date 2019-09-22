from enum import Enum
import numpy as np
import mido
import color
import orientation
#(rows, cols, [midi note mapped, scala cent value, octave/tritave multiplier])
#TODO DECIDE IF INCLUDE TOP ROW BUTTONS
#TODO find math formulae to shift row, column info
#TODO convert to binary


class Launchpad:
    def __init__(self,name, main = False, mode = "XY"):
        self.main = main
        self.mode = mode
        self.orientation = orientation.Orientation.UP
        self.numCol = 9
        self.numRow = 9
        self.leftLP = None
        self.rightLP = None
        self.upLP = None
        self.downLP = None
        self.name = name
        self.MIDInoteArr = self.launchpadSetup()
        # self.portIn = mido.open_input(self.name, callback=self.incomingMessageParser)
        # self.portOut = mido.open_output(self.name)



    #first row is  104-111
    def launchpadSetup(self):
        lpMain = np.zeros((self.numRow , self.numCol), dtype=int)
        rows = self.numRow - 1 
        cols = self.numCol - 1
        start = 0
        step = 0
        for row in range(0,self.numRow,1):
            for col in range(0,self.numCol,1):
                if not (row == rows and col == cols):
                    lpMain[row][col] = 16*row + col #[0] is decimal address 
        #insert last column into first position
        lpMain = np.insert(lpMain,0,lpMain[row],axis = 0)
        lpMain = np.delete(lpMain, row + 1, 0)
        return lpMain
    
    # def incomingMessageParser(self,message):
    #     print(self.name," ",message)
    #     pass


    #TODO implement
    def orientLaunchpad(orientation):
        if orientation == Orientation.UP:
            pass
        elif orientation == Orientation.RIGHT:
            pass
            #Transpose
            #Reverse the rows
        elif orientation == Orientation.LEFT:
            pass
        elif orientation == Orientation.DOWN:
            pass
        else:
            return "Give a valid Orientation"



    def updateAllLED(self, brightnessDecimal,velocities=[]):
        if not len(velocities) == 40:
        #turn on all LEDS
        #send msg 176, 0, brightnessDecimal #125-127 low to bright
            all_on = [176, 0, brightnessDecimal]
            return all_on
        
    #others is a list of other launchpad objects

        




if __name__ == '__main__':
    pass
    #testing creation of 9 x 9 - 1
    #second = Launchpad()
    #print(second.displaymidiNoteNo())
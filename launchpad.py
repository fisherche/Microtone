from enum import Enum
import numpy as np
import mido
import color
from orientation import Orientation
import launchpadLayout
#from launchpadLayout import LaunchpadLayout
#(rows, cols, [midi note mapped, scala cent value, octave/tritave multiplier])
#TODO DECIDE IF INCLUDE TOP ROW BUTTONS
#TODO math formulae to shift row, column info


class Launchpad:
	def __init__(self,name, main = False, mode = "XY"):
		"""
		Class to interface with the MIDI 
		A Novation Launchpad is an 80-button MIDI controller arr. like so:
		XXXXXXXX	<- [8][9] has no button
		XXXXXXXXX
		XXXXXXXXX
		XXXXXXXXX
		XXXXXXXXX
		XXXXXXXXX
		XXXXXXXXX
		XXXXXXXXX
		"""
		self.main = main
		self.mode = mode
		self.orientation = orientation.Orientation.UP
		self.numCol = 9
		self.numRow = 9
		self.name = name
		self.MIDInoteArr = self.launchpadSetup()
		self.layout = None
		# self.portIn = mido.open_input(self.name, callback=self.incomingMessageParser)
		# self.portOut = mido.open_output(self.name)
		#mediator makes self.mediator



	#first row is  [128,135] with none at end, so will need to map down to 104-111
	def launchpadSetup(self):
		rows = self.numRow - 1 
		cols = self.numCol - 1
		lpMain = [[0 for i in range(self.numRow)] for j in range(self.numCol)]
		for row in range(0,self.numRow,1):
			for col in range(0,self.numCol,1):
				if not (row == rows and col == cols):
					lpMain[row][col] = 16*row + col #lpMain[*] is decimal address 
				else:
					lpMain[row][col] = None
		lpMain = [lpMain[rows]] + [lpMain[0]] + lpMain[1:rows]
		return lpMain
	
	def incomingMessageParser(self,message):
		#print(self.name," ",message)
		self.layout.parseIncomingMessage(self.name,message)
		


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
	second = Launchpad('Fake')
	print(second.MIDInoteArr)
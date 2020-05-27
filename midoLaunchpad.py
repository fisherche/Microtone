import mido
from mido import Message
import numpy as np
from multiprocessing import Process, Pipe
from enum import Enum
import launchpad
import launchpadLayout
import FromScala

#TODO: test with fresh install of scl files

class midos:
	def __init__(self):
		self.openmidiinputs = self.scanIO()
		self.lpl.spanAudibleRange(FromScala.readSCL('22equal.scl'))
		#self.lpl.addFlatLattice()
		self.lpl.addFlatLattice(2,3)
		self.lpl.openVirtualOuts()
	#default backend, written in C++, convenient for that transformation
		mido.set_backend('mido.backends.rtmidi')
		print(mido.backend)


	#CONVENTIONS
	#channels from 0 to 15 instead of 1 to 16
	#For LEDs, X-Y layout:
	#origin is topleft corner of grid
	#Hex: Key = (10h x Row) + Columnd
	#Decimal: Key = (16*Row)+ Column
	#scene launch (right) are Column 8,  last is 7
	#
	#

	#Launchpad Programmer's Reference computer-to-launchpad p3
	#Set Grid LEDs: where Key is midi note #
	#Decimal version
	#144, Key, Velocity

	#keep a list of notes in cents. A range of these notes is selected for each line in a layout. Manipulating the layout after creation simply updates the indices. 
	# Create lists of subsets of this list for scales. Generator frequency can be changed in real time.

	#set Grid LED 
	#144, Key, Velocity
	##Input: Green, Red, Flags
	#Flags:
	#12 normal use
	#8 LED flash
	#0 double buffering
	def setVelocity(green,red,flags):
		pass
	def updateAllLED(brightnessDecimal,velocities=[]):
		if not len(velocities) == 40:
			#turn on all LEDS
			#send msg 176, 0, brightnessDecimal #125-127 low to bright
			all_on = [176, 0, brightnessDecimal]
		return all_on
	#return 3-list of note message

	#send message 146, Velocity 1, Velocity 2,
		
	def mapScale(scale):
		
		raise NotImplementedError

	def setDutyCycle(numerator=1,denominator=8):
		if numerator < 9:
			middle = 30
			data = 16 * (numerator - 1) + (denominator - 3)
		else:
			middle = 31
			data = (16* (numerator - 9))+ (denominator - 3)
		return [176, middle, data]

	#key is 
	def setControlLED(key,color):
		if key in range(104,112):
			return [176, key, color]

	def scanIO(self):
		inputs = mido.get_input_names()
		outputs = mido.get_output_names()
		print("input names: ", inputs)
		print("output names: ", outputs)
		openmidiinputs = []
		for i in inputs:
			string = "open " + i + "? Type anything for yes, or just hit enter for no"
			x = input(string)
			if x:
				newDevice = launchpad.Launchpad(i)
				openmidiinputs.append(newDevice)
		self.lpl = launchpadLayout.LaunchpadLayout(openmidiinputs)
		self.lpl.assignAsLayout(openmidiinputs) #to facilitate later changes in layouts
		self.setupPorts()	#instance variable assigned to a Launchpad
		return openmidiinputs
	# def scanIO(self):
	# 	inputs = mido.get_input_names()
	# 	outputs = mido.get_output_names()
	# 	print("input names: ", inputs)
	# 	print("output names: ", outputs)
	# 	self.openmidiinputs = []
	# 	for i in inputs:
	# 		string = "open " + i + "? Type anything for yes, or just hit enter for no"
	# 		x = input(string)
	# 		if x:
	# 			newDevice = Launchpad(i)
	# 			self.openmidiinputs.append(newDevice)
	# 	self.lpl = LaunchpadLayout(self.openmidiinputs)
	# 	return self.openmidiinputs
	def setupPorts(self):
		j = 0
		for i in self.lpl.keypadLst:
			i.portIn = mido.open_input(i.name, callback=i.incomingMessageParser)
			i.portOut = mido.open_output(i.name)
			j += 1
		return


	#TODO rout other launchpads to MIDI virtual inputs 

	def recv_MIDI(conn):
		#blocking statement waits 
		while 1:
			msg = conn.recv()
			if msg == "CLOSE":
				break
		x = conn.recv()



	# port = mido.open_input(mido.get_input_names()[1], callback=LaunchpadLayout.incomingMessageParser0)
	# #portout = mido.open_output(mido.get_output_names()[1])
	# port1 = mido.open_input(mido.get_input_names()[2], callback=LaunchpadLayout.incomingMessageParser0)
	# #portout1 = mido.open_output(mido.get_output_names()[2])



if __name__ == '__main__':
	
	#print("output names: ", mido.get_output_names())
	#port = mido.open_input('Launchpad')
	#launchpadSetup()
	#callback listens without multithreading ?
	#openMIDI = midos.scanIO()
	m = midos()
	#m.scanIO()
	#openMIDI = m.scanIO()
	parent_conn, child_conn = Pipe()
	p = Process(target=midos.recv_MIDI, args=(child_conn,))
	p.start()

	#portout.send_message(updateAllLED(127))
	#ledall = mido.Message.from_bytes(updateAllLED(125))
	#portout.send(ledall)
	

	#port.close()
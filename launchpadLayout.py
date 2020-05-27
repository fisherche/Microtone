import launchpad
from FromScala import readSCL
import mido
from fractions import Fraction
import midiTuningStandardScratchWork

class Scale:
	#TODO: use this class so that launchpadlayout and assoc are scale-agnostic. Generate edos?
	def __init__(self,nameAndNotes):
		self.name, self.notes = nameAndNotes


#TODO populateObjList and keypadReverseNameLookup at same time, more meaningful name
class Instrument:

	def __init__(self,scl=None):
		pass

class LaunchpadLayout:

	"""
	Terminology:
	scale : a repeated series of pitch values (usually a tuning or a temperament)
	subscale : a user-chosen sequence that defaults to the entire scale #TODO integrate
	"""
	def __init__(self,lpLst,scl=None):
		#main launchpad is keypadLst[0]
		self.keypadLst = lpLst
		self.keypadReverseNameLookup = self.populateKeypadReverseNameLookup()
		self.controlButtons = {}
		
		self.lpMapLookupLinear, self.numKeys, self.rowLengths = self.mapIncomingToLinearNumbers() #self.rowLengths is a [#row0, #row1,#row2], so len(self.rowLengths) gives #cols
		self.scale = scl #use spanAudibleRange to populate
		#					list of note values as note = [interval,multiplier] = interval*multiplier
		self.scaleDescr = None
		self.parent_conn = None
		self.latticeIndex = 0 #call addFlatLattice to populate
		self.flatNoteNumberLattices = []

		self.basisFreq = 440 
		self.virtualOuts = []
		#self.setupPorts()

	def addToKeypadLst(self,lp):
		"""
		utility method for updating the dictionary, used to reverse lookup Controller Name
		"""
		self.keypadLst += [lp]
		self.populateKeypadReverseNameLookup()
		return 


	def populateKeypadReverseNameLookup(self):
		"""
		keypadArrangement: Dict used to look up index of incoming button pressess
		#TODO: remove dependencies
		"""
		keypadReverseNameLookup = {}
		for i in range(len(self.keypadLst)):
			keypadReverseNameLookup[self.keypadLst[i].name] = i
		return keypadReverseNameLookup
			
	def addFlatLattice(self,horizontalBasis=1,verticalBasis=5):
		"""
		populates self.flatNoteNumberLattices
		PARAMETERS:
		verticalBasis : int number of steps
		horizontalBasis : default 1
		RETURNS :
		a list whose indices are sequential MIDI numbers (but if > 128,not valid)
			value at an index is the index of a note in self.scale

		"""
		if self.scale is None:
			print("self.scale is None. Assign a scale before trying to map it.")
			return 
		outLst = [None for i in range(self.numKeys)]
		listIndex = 0
		scaleIndex = 0
		for row in range(len(self.rowLengths)):
			currentRowLength = self.rowLengths[row]
			rowStartIndex = scaleIndex
			for _ in range(currentRowLength):
				if scaleIndex < len(self.scale): 
					outLst[listIndex] = scaleIndex
					scaleIndex += horizontalBasis
					listIndex += 1
				else:
					break

			scaleIndex = rowStartIndex + verticalBasis
		self.flatNoteNumberLattices += [outLst]
		return outLst

	def parseIncomingMessage(self,senderName,message):
		#print(senderName,message)
		messageBytes = message.bytes()
		lp = self.keypadReverseNameLookup[senderName]
		#print("name", senderName, "lp", lp)
		outIndex= self.lpMapLookupLinear[lp][messageBytes[1]]
		#use outIndexToSendToOutput
		#print(senderName,messageBytes[1]," ",outIndex)
		self.sendToOutputChannel(messageBytes,outIndex)

	def sendToOutputChannel(self,messageBytes,bigMIDInumber):
		#TODO: clean
		bigMIDInumber = self.flatNoteNumberLattices[self.latticeIndex][bigMIDInumber]

		for i in range(len(self.virtualOuts)):
			if bigMIDInumber < (i+1)*128:	#seive
				regularMIDI = bigMIDInumber - (i)*128
				#print("messagebytes",messageBytes)
				if messageBytes[2] == 127:
					tempered = 64
				else:
					tempered = 0
				mess = mido.Message(type='note_on',note=regularMIDI, velocity=tempered)#TODO take out hardcoded
				print("mess",mess)
				self.virtualOuts[i].send(mess)
				print("sendSuccessful",self.virtualOuts[i])
				break


	#TODO
	# based on self.scale
	#RETURNS:
	# number of virtual outputs and .mid files needed
	# list of .MID Tuning dump filenames
	def buildMIDIoutAllAudibleNotes(self):
		midiTuningStandardScratchWork.convertFreqToPitchBendBytes()
		pass

	#TODO: change dictionary/list population to reflect this
	def assignAsLayout(self,lpObjects):
		for lp in lpObjects:
			lp.layout = self
		return

	

	def recv_msg(self,msg):
		while 1:
			msg = conn.recv()
			if msg == 'END':
				break
			print("somehow rcv",msg)


	#populates lpMapLookup and gives the number of notes
	#first row is  [128,135] with none at end, so will need to map down to 104-111
	#RETURNS:
	# lpMapLookup : a list whose items are dictionaries for ea Launchpad
	def mapIncomingToLinearNumbers(self):
		#from left to right in lpLst
		lpMapLookup = [{} for ea in self.keypadLst]
		mainLp = self.keypadLst[0]
		MIDInoteCounter = 0
		rowLengths = []
		for row in range(len(mainLp.MIDInoteArr)-1,-1,-1):
			rowLen = 0
			for lp in range(len(self.keypadLst)):
				for horizontalStep in self.keypadLst[lp].MIDInoteArr[row]:
					if (lp is mainLp) and (horizontalStep >= 121):
						lpMapLookup[lp][horizontalStep] = None
					elif horizontalStep == None:
						pass
					else:
						lpMapLookup[lp][horizontalStep] = MIDInoteCounter
					rowLen+= 1
					MIDInoteCounter += 1
			rowLengths += [rowLen]
		return lpMapLookup, MIDInoteCounter + 1,rowLengths


	
	def spanAudibleRange(self,scale, low=20,high= 9000,middle=440):
		scaleCount = 0
		output = []
		scaleIntervals = scale[1]
		lenScale = len(scaleIntervals)
		self.scaleDescr = scale[0]
		self.scale = scale[1]
		
		lowest = middle
		while lowest > low:
			lowest = lowest/2
		multiplier = 1
		currOctaveNote = lowest
		parallelPitchClass = []
		while currOctaveNote < high:
			for i in range(len(scaleIntervals)):
				currInterval = scaleIntervals[i]
				currFreq = currOctaveNote*currInterval
				#output += [[currInterval,multiplier]]
				output += [currFreq]
				parallelPitchClass += [currInterval,multiplier]
			currOctaveNote = currFreq
			multiplier += 1

		self.scale = output
		return output,parallelPitchClass
	
	
	#copied from midoLaunchpad for unit testing	
	# #TODO try except finally	
	def scanIO():
		inputs = mido.get_input_names()
		outputs = mido.get_output_names()
		print("input names: ", inputs)
		print("output names: ", outputs)
		openMIDIlst = []
		for i in inputs:
			string = "open " + i + "? Type anything for yes, or just hit enter for no"
			x = input(string)
			if x:
				newDevice = launchpad.Launchpad(i)
				openMIDIlst.append(newDevice)
		return openMIDIlst   

	def openVirtualOuts(self):
		#TODO: try, except
		self.scale #spansAudibleRange
		i = 0
		while i < len(self.scale):
			name = "Instrument" + str(i)
			virtualOut = mido.open_output(name,virtual=True)#initialize virtual output
			#virtualOut = mido.open_output("IAC Driver IAC Bus 2")
			self.virtualOuts += [virtualOut]
			i += 128
		return

	
	def __repr__(self):
		#TODO
		raise NotImplementedError
	def __str__(self):
		#display the matrix
		out = ""
		
		out += "keypadLst " + str(self.keypadLst) + "\n"
		out += "keypadReverseNameLookup " + str(self.keypadReverseNameLookup) + "\n"
		out += "controlButtons " + str(self.controlButtons) + '\n'
		
		out += "self.lpMapLookupLinear " + str(self.lpMapLookupLinear) + "\n"
		out += "self.numKeys " + str(self.numKeys) + "\n"
		
		out += "self.scale " + str(self.scale) + "\n" #use spanAudibleRange to populate
		return out


class KeyboardLayout:
	def __init__(self):
		#TODO:
		pass




if __name__ == '__main__':
	test = LaunchpadLayout(LaunchpadLayout.scanIO())
	#TODO: Tests for note lists
	for i in test.spanAudibleRange(readSCL('twelveEqual.scl')):
		print(i[0]*i[1]*440)
		pass
	print(test.addFlatLattice(5)) #P4
	print(test)
	
	#print(test.scale)
	#print(test.layout)
	#print(test.lpMapLookup)

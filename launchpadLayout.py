import launchpad
import FromScala
import mido
from fractions import Fraction
import midiTuningStandardScratchWork

#TODO populateObjList and ObjDict at same time
class LaunchpadLayout:
	def __init__(self,lpLst,scl=None):
		#main launchpad is objLst[0]
		self.objLst = lpLst
		self.objDict = self.populateObjDict()
		self.controlButtons = {}
		
		self.lpMapLookupLinear, self.numNotes,self.rowLengths = self.mapIncomingToLinearNumbers() 
		self.scale = None #use spanRangeByIntervals to populate
		#					list of note values as note = [interval,multiplier] = interval*multiplier
		self.scaleDescr = None
		self.parent_conn = None
		self.layout = None #call mapLinearNumbersTo2DLattice to populate
		self.basisFreq = 440 
		self.virtualOuts = []
		#self.setupPorts()

	def addToObjLst(self,lp):
		self.objLst += [lp]
		self.populateObjDict()
		return 

	
	def populateObjDict(self):
		objDict = {}
		for i in range(len(self.objLst)):
			objDict[self.objLst[i].name] = i
		return objDict

	def parseIncomingMessage(self,senderName,message):
		print(senderName,message)
		messageBytes = message.bytes()
		lp = self.objDict[senderName]
		print("name", senderName, "lp", lp)
		outIndex= self.lpMapLookupLinear[lp][messageBytes[1]]
		#use outIndexToSendToOutput
		print(senderName,messageBytes[1]," ",outIndex)
		self.sendToOutputChannel(messageBytes,outIndex)

	def sendToOutputChannel(self,messageBytes,bigMIDInumber):

		for i in range(len(self.virtualOuts)):
			if bigMIDInumber < (i+1)*128:	#seive
				regularMIDI = bigMIDInumber - (i)*128
				print("messageby",messageBytes)
				if messageBytes[2] == 127:
					tempered = 64
				else:
					tempered = 0
				mess = mido.Message(type='note_on',note=regularMIDI, velocity=tempered)#TODO take out hardcoded
				print("mess",mess)
				self.virtualOuts[i].send(mess)
				print("sendSuccessful")
				break
	#to advise user on the max vertical distance to use all notes
	#given horizontal step is 1
	#TODO 
	def largestVerticalStep(self):
		if self.scale is not None:
			highestInScale = len(self.scale) - 1
		else:
			print("self.scale is None. Update scale before finding largest Vertical step")
			return
		

			
	#populates self.layout
	#PARAMETERS:
	# vertical : int number of steps
	# horizontal : default 1
	#RETURNS :
	# a list whose indices are sequential MIDI numbers (but if > 128,not valid)
	# 	value at an index is the index of a note in self.scale
	def mapLinearNumbersTo2DLattice(self,vertical,horizontal=1):
		#for each row
			#look up linear notes
			#if noteCounter % rowLengths[i] == 0:
				#next linear note is a vertical step up
			#mod by rowLengths[i]
		if self.scale is None:
			print("self.scale is None. Assign a scale before trying to map it.")
			return 
		outLst = [None for i in range(self.numNotes)]
		listIndex = 0
		scaleIndex = 0
		for row in range(len(self.rowLengths)):
			currRowLen = self.rowLengths[row]
			rowStartIndex = scaleIndex
			for i in range(currRowLen):
				if scaleIndex < len(self.scale): #means there's a value here
					outLst[listIndex] = scaleIndex
					scaleIndex += (1*horizontal)
					listIndex += 1
				else:
					break

			scaleIndex = rowStartIndex + vertical
		self.layout = outLst
		return outLst

	def remapLatticeRight(self):
		pass
	def remapLatticeLeft(self):
		pass
	def remapLatticeUp(self):
		pass
	def remapLatticeDown(self):
		pass

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
		lpMapLookup = [{} for ea in self.objLst]
		mainLp = self.objLst[0]
		MIDInoteCounter = 0
		rowLengths = []
		for row in range(len(mainLp.MIDInoteArr)-1,-1,-1):
			rowLen = 0
			for lp in range(len(self.objLst)):
				for sequentialNote in self.objLst[lp].MIDInoteArr[row]:
					if (lp == mainLp) and (sequentialNote >= 121):
						lpMapLookup[lp][sequentialNote] = None
					elif sequentialNote == None:
						pass
					else:
						lpMapLookup[lp][sequentialNote] = MIDInoteCounter
					rowLen+= 1
					MIDInoteCounter += 1
			rowLengths += [rowLen]
		return lpMapLookup, MIDInoteCounter + 1,rowLengths

	#updates self.scale
	#updates self.basisFreq
	#returns a list of note values as note = [interval,multiplier] = interval*multiplier
	# def spanRangeByIntervals(self,scale,low=20,high=9000, middle = 440):
	# 	self.basisFreq = middle
	# 	self.scaleDescr = scale[0]
	# 	self.scale = scale[1]
	# 	scaleIntervals = scale[1]
	# 	basisNote = 1
	# 	indexBasisNote = 0
	# 	#[note, multiplier] means eg 1/1 * multiplier 
	# 	output = [[basisNote,1]]
	# 	currFreq = float(middle * scaleIntervals[0])
	# 	scaleCount = 0
	# 	lenScale = len(scaleIntervals)
	# 	up = self.spanRangeUp(basisNote,scaleIntervals,lenScale,high,middle)
	# 	down = self.spanRangeDown(basisNote,scaleIntervals,lenScale,low,middle)
	# 	output = down + output + up
	# 	indexBasisNote = len(down)
	# 	self.scale = output
	# 	return indexBasisNote, output

	def spanRangeByIntervals(self,scale, low=20,high= 9000,middle=440):
		scaleCount = 0
		output = []
		scaleIntervals = scale[1]
		lenScale = len(scaleIntervals)
		self.scaleDescr = scale[0]
		self.scale = scale[1]
		
		# while currFreq < high:
		# 	currInterval = scaleInterv[scaleCount % lenScale]
		# 	multiplier = (scaleCount // lenScale) + 1
		# 	print(currInterval*multiplier)
		# 	output.append([currInterval,multiplier])
		# 	currFreq = float(middle * currInterval * multiplier)
		# 	scaleCount += 1
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

		for i in output:
			print(i)
			pass	
		self.scale = output
		return output,parallelPitchClass
	def spanRangeDown(self,basisNote, scaleInterv,lenScale,low,middle):
		# scaleCount = 0
		# currFreq = middle
		# scaleCount = 2
		# output = []
		# while currFreq > low:
		# 	#str
		# 	currInterval = scaleInterv[(lenScale - scaleCount) % lenScale]
		# 	multiplier = 1/((scaleCount // lenScale) + 2)
		# 	output.insert(0,[currInterval,multiplier])
		# 	currFreq = float(middle * currInterval * multiplier)
		# 	#print(currFreq, currInterval,scaleCount,lenScale)
		# 	scaleCount += 1
		# #print(output)
		lowest = middle
		while lowest > low:
			lowest = lowest/2
		scaleCount = 0
		currFreq = lowest
		scaleCount = 0
		output = []
		while currFreq < middle:
			currInterval = scaleInterv[scaleCount % lenScale]
			multiplier = (scaleCount // lenScale) + 1
			output.append([currInterval,multiplier])
			currFreq = float(lowest * currInterval * multiplier)
			scaleCount += 1
		# for i in output:
		# 	print(i[0]*i[1]*lowest)
		return output
	


				

	#copied from midoLaunchpad for unit testing		
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
		#removed circular ref
		#LaunchpadLayout()
		return openMIDIlst   

	def openVirtualOuts(self):
		self.scale #spansAudibleRange
		i = 0
		while i < len(self.scale):
			name = "Instrument" + str(i)
			virtualOut = mido.open_output(name,virtual=True)#initialize virtual output
			#virtualOut = mido.open_output("IAC Driver IAC Bus 2")
			self.virtualOuts += [virtualOut]
			i += 128
		return
			





if __name__ == '__main__':
	test = LaunchpadLayout(LaunchpadLayout.scanIO())
	for i in test.spanRangeByIntervals(FromScala.readSCL('twelveEqual.scl')):
		#print(i[0]*i[1]*440)
		pass
	print(test.mapLinearNumbersTo2DLattice(5)) #P4
	
	#print(test.scale)
	#print(test.layout)
	#print(test.lpMapLookup)

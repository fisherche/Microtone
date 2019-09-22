from launchpad import Launchpad
import FromScala
import mido
from fractions import Fraction
class LaunchpadLayout:
	def __init__(self,lpLst):
		#main launchpad is lpObjLst[0]
		self.lpObjLst = lpLst
		self.lpObjDict = self.populatelpObjDict()
		self.controlButtons = {}
		self.lpMapLookup = [{} for ea in self.lpObjLst]
		self.mapIncomingToKeyboardLayout()
		self.scale = None
		self.scaleDescr = None
		self.parent_conn = None
		self.hardCodedFunctions = {'self.incomingMessageParser0': self.incomingMessageParser0,
		'self.incomingMessageParser1': self.incomingMessageParser1}
		#self.setupPorts()


	
	def populatelpObjDict(self):
		lpObjDict = {}
		for i in range(len(self.lpObjLst)):
			lpObjDict[self.lpObjLst[i].name] = i
		return lpObjDict
	def incomingMessageParser0( message):
		#change
		print("0", message)

	def incomingMessageParser1(self,message):
		print("1", message)

	
	def setupPorts(self):
		j = 0
		for i in self.lpObjLst:
			callbackName = "self.incomingMessageParser"+str(j)
			callb = self.hardCodedFunctions[callbackName]

			#lambda does not seem to work
			#a = lambda msg: self.toMIDIout(i.name, msg.bytes())
			#i.portIn = mido.open_input(i.name, callback=a)

			i.portIn = mido.open_input(i.name, callback=self.incomingMessageParser0)
			i.portOut = mido.open_output(i.name)
			j += 1
		return


	def toMIDIout(self,name,messageBytes):
		byte2 = messageBytes[1]
		lp = self.lpObjDict[name]
		print("name",name,"lp", lp)
		outNote = self.lpMapLookup[lp][byte2]
		print(name,byte2," ",outNote)
		#print(messageBytes)


	def recv_msg(self,msg):
		while 1:
			msg = conn.recv()
			if msg == 'END':
				break
			print("somehow rcv",msg)


	#populates lpMapLookup
	def mapIncomingToKeyboardLayout(self):
		#from left to right in lpLst
		mainLp = self.lpObjLst[0]
		MIDInoteCounter = 0
		for row in range(len(mainLp.MIDInoteArr)-1,-1,-1):
			for lp in range(len(self.lpObjLst)):
				for sequentialNote in self.lpObjLst[lp].MIDInoteArr[row]:
					if (lp == mainLp) and (sequentialNote >= 121):
						self.lpMapLookup[lp][sequentialNote] = None
					else:
						self.lpMapLookup[lp][sequentialNote] = MIDInoteCounter
					MIDInoteCounter += 1
		print(self.lpMapLookup)
		return
	#returns a list of note values as note = [interval,multiplier] = interval*multiplier
	def spanRangeByIntervals(self,scale,low=8,high=14000, middle = 440):
		self.scaleDescr = scale[0]
		self.scale = scale[1]
		scaleIntervals = scale[1]
		basisNote = 1
		indexBasisNote = 0
		#[note, multiplier] means eg 1/1 * multiplier 
		output = [[basisNote,1]]
		curr = float(middle * scaleIntervals[0])
		scaleCount = 0
		lenScale = len(scaleIntervals)
		up = self.spanRangeUp(basisNote,scaleIntervals,lenScale,curr,high,middle)
		down = self.spanRangeDown(basisNote,scaleIntervals,lenScale,curr,low,middle)
		output = down + output + up
		indexBasisNote = len(down)
		print(output)
		return indexBasisNote, output

	def spanRangeUp(self,basisNote, scaleInterv,lenScale,firstInterval,high,middle):
		scaleCount = 0
		curr = firstInterval
		scaleCount = 0
		output = []
		while curr < high:
			#str
			currInterval = scaleInterv[scaleCount % lenScale]
			multiplier = (scaleCount // lenScale) + 1
			output.append([currInterval,multiplier])
			curr = float(middle * currInterval * multiplier)
			scaleCount += 1
		return output
	def spanRangeDown(self,basisNote, scaleInterv,lenScale,firstInterval,low,middle):
		scaleCount = 0
		curr = firstInterval
		scaleCount = 0
		output = []
		while curr > low:
			#str
			currInterval = scaleInterv[(lenScale - scaleCount) % lenScale]
			multiplier = 1/((scaleCount // lenScale) + 1)
			output.insert(0,[currInterval,multiplier])
			curr = float(middle * currInterval * multiplier)
			scaleCount += 1
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
				newDevice = Launchpad(i)
				openMIDIlst.append(newDevice)
		#removed circular ref
		#LaunchpadLayout()
		return openMIDIlst       


if __name__ == '__main__':
	test = LaunchpadLayout(LaunchpadLayout.scanIO())
	test.mapIncomingToKeyboardLayout()
	test.spanRangeByIntervals(FromScala.readSCL('dorian_tri2.scl'))
	#print(test.lpMapLookup)

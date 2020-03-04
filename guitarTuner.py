import sounddevice
import numpy as np 
import time

class AudioDevice():
    def __init__(self):
        self.sampleFreq = 44100
        self.amplification = 0.4 #TODO add additional attunation w/r/t intensity
        self.duration = 4


    def makeAudible(self,frequency, duration=None):
        if duration == None:
            duration = self.duration
        samples = np.arange(duration,self.sampleFreq)/ self.sampleFreq
        
        waveform = np.sin(2* np.pi * samples * frequency)
        waveScaled = waveform * self.amplification
        sounddevice.play(waveScaled,self.sampleFreq)
        time.sleep(duration)
        sounddevice.stop()
    
class ED2Instrument():
    def __init__(self,numberOfStrings):
        self.ed2 = None
        self.referenceHz = None
        self.resonator = AudioDevice()
        self.openNotes = [0]*numberOfStrings #List that stores open string note indices

        self.strings = [] #List that stores lists of playable notes


    #returns a list of cent values
    def generateAssignED2(self,slices, referenceHz=440, lowestHz=20, highestHz = 3000):

        #calculate which key the reference is
        key = 0

        if referenceHz < lowestHz:
            print("Reference lower than lowest allowable")
            return
        if referenceHz > highestHz:
            print("Reference lower than lowest allowable")
            return
        currentHz = referenceHz*(2**(1/slices))
        ed2List = []
        keyExponent = 0
        while currentHz > lowestHz:
            currentHz = referenceHz*(2**(1/slices))**(keyExponent)
            ed2List = [currentHz] + ed2List 
            keyExponent -= 1
        highHz = referenceHz*(2**(1/slices)) 
        referenceNoteNo = -1 * keyExponent
        keyExponent = 0
        while highHz < highestHz:
            keyExponent += 1
            highHz = referenceHz*(2**(1/slices))**(keyExponent)
            ed2List = ed2List + [highHz]
        self.ed2 = ed2List
        self.referenceNoteNo = referenceNoteNo
        self.referenceHz = referenceHz
        return ed2List,referenceNoteNo

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


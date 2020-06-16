import math
stdMIDIfrequencies = [16.35,17.32,18.35,19.45,20.60,21.83,23.12,24.50,25.96,27.50,29.14,30.87,32.70,34.65,36.71,38.89,41.20,43.65,46.25,49.00,51.91,55.00,58.27,61.74,65.41,69.30,73.42,77.78,82.41,87.31,92.50,98.00,103.83,110.00,116.54,123.47,130.81,138.59,146.83,155.56,164.81,174.61,185.00,196.00,207.65,220.00,233.08,246.94,261.63,277.18,293.66,311.13,329.63,349.23,369.99,392.00,415.30,440.00,466.16,493.88,523.25,554.37,587.33,622.25,659.25,698.46,739.99,783.99,830.61,880.00,932.33,987.77,1046.50,1108.73,1174.66,1244.51,1318.51,1396.91,1479.98,1567.98,1661.22,1760.00,1864.66,1975.53,2093.00,2217.46,2349.32,2489.02,2637.02,2793.83,2959.96,3135.96,3322.44,3520.00,3729.31,3951.07,4186.01,4434.92,4698.63,4978.03,5274.04,5587.65,5919.91,6271.93,6644.88,7040.00,7458.62,7902.13]
A4 = 440
A4MIDInumber = 69

barr = []




#print(barr)

barr1 = []
offset12 = 151 #guess of first note
o = 0
with open("Tunings/12equal.mid",'rb') as b:
    byte = b.read(1)
    o += 1
    notesLst = []
    while byte != b"":
        barr1.append(byte)
        o +=1
        while o >= 152 and byte != b"":
            
            packet = []
            for i in range(3):
                byte = b.read(1)
                packet += [byte]
                o += 1
            notesLst += [packet]
            #start building the three byte note packets 
        #print(notesLst)
        byte = b.read(1)

o = 0
barr1 = []
with open("Tunings/24equal.mid",'rb') as b:
    byte = b.read(1)
    o += 1
    notesLst = []
    while byte != b"":
        barr1.append(byte)
        o +=1
        while o >= 149 and byte != b"":
            
            packet = []
            for i in range(3):
                byte = b.read(1)
                packet += [byte]
                o += 1
            notesLst += [packet]
            #start building the three byte note packets 
        #print(notesLst)
        byte = b.read(1)

#startpos 24edo: 148 +1
#startpos 12edo: 151
def extractNotesBytes(file, startPos):
    o = 0
    barr1 = []
    with open("Tunings/"+file,'rb') as b:
        byte = b.read(1)
        o += 1
        notesLst = []
        notesCounter = 0
        while byte != b"":
            barr1.append(byte)
            o +=1
            while o >= startPos  and byte != b"":
                
                packet = []
                for i in range(3):
                    byte = b.read(1)
                    packet += [byte]
                    o += 1
                notesLst += [packet]
                notesCounter += 1
                #start building the three byte note packets 
            byte = b.read(1)
    return notesLst

#print(notesLst)
#print(barr1)
def convertPitchBendBytesToCents(mm,nn):
    return (128*int(mm.hex(),16) + int(nn.hex(),16))/163.84


def convertCentsToPitchBendBytes(cents):
    #TODO
    pass
#PARAMETERS:
#freq is a frequency in Hz
#midiKeyNumber is an int in [0,127] to account for frequency == midi note frequency the 'no change' situation
def convertFreqToPitchBendBytes(freq):
    #TODO
    #7F 7F 7F means no change for that midi key number
    #find nearest midi note below frequency
    #
    #7F 7F 7F means no change for that midi key number
    nearestMIDI = math.floor(12*math.log(freq/A4,2)+A4MIDInumber)
    print(nearestMIDI)
    if nearestMIDI > 127:
        print("frequency too high")
    else:
        byte1 = nearestMIDI
        #cents = convertFreqToCents()
        #convert cents 
        #get byte 2 and byte 3
        


    # if round(nearestMIDI,2) == 
    pass





def buildDummyNotesLst(indexStart,noteStart,indexEnd,noteEnd):
    outp = [[0,0,0] for __ in range(128)]
    for i in range(128):
        if i == indexStart:
            outp[i] = noteStart
        if i == indexEnd:
            outp[i] = noteEnd
    return outp


def injectNotes(filename,startPos,replacementNotes):
    o = 0
    barr1 = []
    with open("Tunings/"+filename+"COPY"+".mid",'wb') as cp:
        with open("Tunings/"+filename+".mid",'rb') as b:
            byte = b.read(1)
            #print(byte)
            cp.write(byte)
            o += 1
            notesLst = []
            notesCounter = 0
            notesIndex = 0
            while byte != b"":
                barr1.append(byte)
                o +=1
                while o >= startPos  and notesIndex < len(replacementNotes):         
                    packet = []
                    for i in range(3):
                        #add replacementNotes[i]
                        byte = b.read(1)
                        packet += [byte]
                        newByte = replacementNotes[notesIndex][i].to_bytes(1,byteorder='big')
                        #print(byte," its replacement ", newByte, " from ",replacementNotes[notesIndex][i])
                        cp.write(newByte)
                        o += 1
                    notesLst += [packet]
                    notesCounter += 1
                    #print(notesCounter)
                    notesIndex += 1
                byte = b.read(1)
                cp.write(byte)
    
    return

#print(buildDummyNotesLst(0,[60,0,60],127,[60,0,60]))


def injectNotes(filename,startPos,replacementNotes):
    o = 0
    barr1 = []
    with open("Tunings/"+filename+"COPY"+".mid",'wb') as cp:
        with open("Tunings/"+filename+".mid",'rb') as b:
            byte = b.read(1)
            #print(byte)
            cp.write(byte)
            o += 1
            notesLst = []
            notesCounter = 0
            notesIndex = 0
            while byte != b"":
                barr1.append(byte)  
                o +=1
                while o >= startPos  and notesIndex < len(replacementNotes):           
                    packet = []
                    for i in range(3):
                        #add replacementNotes[i]
                        byte = b.read(1)
                        packet += [byte]
                        newByte = replacementNotes[notesIndex][i].to_bytes(1,byteorder='big')
                        #print(byte," its replacement ", newByte, " from ",replacementNotes[notesIndex][i])
                        cp.write(newByte)
                        o += 1
                    notesLst += [packet]
                    notesCounter += 1
                    #print(notesCounter)
                    notesIndex += 1
                byte = b.read(1)
                cp.write(byte)
    
    return

def humanReadableNotesList(notesLst):
    outp = []
    for i in notesLst:
        zero = int(i[0].hex(),16)
        cents = convertPitchBendBytesToCents(i[1],i[2])
        outp.append([zero,cents])
    return outp


#please help me figure out what the d and e means. Blank space against a list of notes officially full of this? 
def compareNoteArrays(file1,offset1,file2,offset2):
    arr1 = extractNotesBytes(file1,offset1)
    arr2 = extractNotesBytes(file2,offset2)
    matches = []
    split = False
    for i in range(len(arr1)-1,-1,-1):
        #print(i)
        if arr1[i] == arr2[i]:
            if split:
                matches = [None] + matches 
                split = False
            matches = [(i,arr1[i])] + matches
        else:
            split = True
    return matches


def main():
    print(compareNoteArrays('12equal.mid',152,'24equal.mid',152))
    print(injectNotes("12equal",152,buildDummyNotesLst(0,[60,0,60],127,[60,0,60]))) #maps 
    #print(humanReadableNotesList(extractNotesBytes('12equal.mid',152)))
    #print(humanReadableNotesList(extractNotesBytes('24equal.mid',152)))
    #print(humanReadableNotesList(extractNotesBytes('313equal.mid',153)))
    #print(humanReadableNotesList(extractNotesBytes('60equal.mid',152)))
    #print(extractNotesBytes('60equal.mid',152))



if __name__ == __main__:
    main()

    









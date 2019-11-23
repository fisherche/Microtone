

#r = open("Tunings/19equala440.mid",'r')
#rea = r.read()
#r.close()
#b = open("Tunings/19equala440.mid",'rb')
barr = []


with open("Tunings/24equal.mid",'rb') as b:
    byte = b.read(1)
    while byte != b"":
        barr.append(byte)
        byte = b.read(1)


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
def convertFreqToPitchBendBytes(basisFreq):
    #TODO
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
injectNotes("12equal",152,buildDummyNotesLst(0,[60,0,60],127,[60,0,60]))

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

#print(humanReadableNotesList(extractNotesBytes('12equal.mid',152)))
#print(humanReadableNotesList(extractNotesBytes('24equal.mid',152)))
#print(humanReadableNotesList(extractNotesBytes('313equal.mid',153)))
#print(humanReadableNotesList(extractNotesBytes('60equal.mid',152)))
#print(extractNotesBytes('60equal.mid',152))


#please help me figure out what the d and e means. Blank space against a list of notes officially full of this? 
def compareNoteArrays(file1,offset1,file2,offset2):
    arr1 = extractNotesBytes(file1,offset1)
    arr2 = extractNotesBytes(file2,offset2)
    matches = []
    split = False
    for i in range(len(arr1)-1,-1,-1):
        print(i)
        if arr1[i] == arr2[i]:
            if split:
                matches = [None] + matches 
                split = False
            matches = [(i,arr1[i])] + matches
        else:
            split = True
    return matches
print(compareNoteArrays('12equal.mid',152,'24equal.mid',152))



    



    









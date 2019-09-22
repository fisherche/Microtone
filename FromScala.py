import os 
from fractions import Fraction
import math
#read .scl files
#FUTURE: .kbm for loading keboard mappings
#parse them per definition


# ! /Users/Fisher 1/Desktop/twelveEqual.scl
# !
# twelveEqual
#  12
# !
#  100.00000
#  200.00000
#  300.00000
#  400.00000
#  500.00000
#  600.00000
#  700.00000
#  800.00000
#  900.00000
#  1000.00000
#  1100.00000
#  2/1

#TODO system agnostic paths
#TODO function that opens a file from explorer
def readSCL(afile):
    """
    Parses a given Scala file (.scl) to a description and its interval values

    Parameters:
    afile (str): file name or relative or absolute path

    Returns:
    as a tuple:
    descr (str): optional description of scale
    scaleLst (list of str): (prepended by the number of notes in the scale) comma-separated cent values (denoted by '.') or intervals (denoted by absence of '.' or by '/'). 
    Following Scala convention, 1/1 or 0 cents, unison, is omitted. 
    """
    scaleLst = []
    if not os.path.isabs(afile):
        #TODO ensure runs from app level...
        path = os.path.join(os.getcwd(),'scalaFiles/scl/',afile)
    else:
        path = file
    f = open(path,'r')
    peskyFirstLine = True

    for line in f:
        if line[0] == '!':
            continue
        if peskyFirstLine:
            descr = line[:-1] 
            peskyFirstLine = False
            continue
        #'!' denotes comment
        pitchVal = ""
        for c in line:
            if c.isspace():
                if not (pitchVal == ""):

                    scaleLst.append(pitchVal)
                
                continue
            else:
                pitchVal += c 
    f.close()
    scaleUsable = makeScaleUsable(scaleLst)
    return (descr, scaleUsable)
		
def centsToInterval(cents):
    return 2**(cents/1200)

def makeScaleUsable(scaleLst):
    usableLst = []
    for i in scaleLst:
        if '/' in i:
            newI = Fraction(i)
            usableLst.append(newI)
        else:
            usableLst.append(centsToInterval(float(i)))
    return usableLst
            



    def midiMapKeyboard():
        pass

if __name__ == '__main__':
    #TODO test with all files
    print(readSCL('dorian_tri2.scl'))
    #print(frequencyListFromNoteAndScale(440,'twelveEqual.scl'))
#cents(frq1,frq2) = 1200 * log2(b/a)
#cents(ratio) = 1200 * log2(ratio)
#note(ref freq, cents) = reffreq*2^(cents/1200)
#ratio of 1 cent is approx 1.0005777895


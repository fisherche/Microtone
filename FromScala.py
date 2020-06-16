import os 
from fractions import Fraction
import math
#TODO instruct user to put .scl or .kbm files in ScalaFiles
#Scala: http://www.huygens-fokker.org/scala/ : the most popular tuning repository and generator and keyboard mapper
#PURPOSE: read .scl files 
#FUTURE: .kbm for loading keboard mappings
#parse them per definition

# ! /twelveEqual.scl
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

#TODO system-agnostic paths
#TODO function that opens a file from explorer
def readSCL(afile):
    """
    Parses a given Scala file (.scl) to a description and its interval values

    Parameters:
    afile (str): file name or relative or absolute path

    Returns: (descr, scaleLst)
    descr (str): optional description of scale
    scaleLst (list of str): (prepended by the number of notes in the scale) comma-separated cent values (denoted by '.') or intervals (denoted by absence of '.' or by '/'). 
    Following Scala convention, the first ratio, 0 cents or 1/1, is omitted. 
    """
    scaleLst = []
    if not os.path.isabs(afile):
        path = os.path.join(os.getcwd(),'ScalaFiles',afile)
    else:
        path = afile
    f = open(path,'r')
    peskyFirstLine = True
    peskySecondLine = True
    for line in f:
        if line[0] == '!':
            continue
        if peskyFirstLine:
            descr = line[:-1] 
            peskyFirstLine = False
            continue
        if peskySecondLine:
            peskySecondLine = False
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
    #print("scaleLst",scaleLst)
    def makeScaleUsable(scaleLst):
        usableLst = [None for i in range(len(scaleLst))]
        for i in range(len(scaleLst)):
            if '/' in scaleLst[i]:
                #we've encountered a fraction 
                newI = Fraction(scaleLst[i])
                usableLst[i] = newI
            else:
                usableLst[i] = centsToInterval(float(scaleLst[i]))
        return usableLst
    scaleUsable = makeScaleUsable(scaleLst)
    return (descr, scaleUsable)
		
def centsToInterval(cents):
    """
    cents congruent mod 1200 are "equivalent"
    """
    return 2**(cents/1200)
def setPathToScalaFiles():
    #TODO
    raise NotImplementedError


if __name__ == '__main__':
    pass
    #TODO test with all files
    #print(readSCL('twelveEqual.scl'))
    #print(readSCL('twelveEqual.scl'))
    #print(frequencyListFromNoteAndScale(440,'twelveEqual.scl'))



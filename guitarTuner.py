

class ED2Instrument():
    def __init__(self,numberOfStrings):
        self.numberOfStrings = numberOfStrings
    #returns a list of cent values
    def generateED2(slices, referenceHz, lowestHz=20, highestHz = 3000):

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
        return ed2List,referenceNoteNo

    print(generateED2(12,440))
            

            

    def generateFretboard(self,numberOfStrings):
        



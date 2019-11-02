import numpy 
import matplotlib.pyplot as plt

def plotLCMinRange(x,length):
    xs = [i for i in range(length)]
    ys = []
    for i in range(len(xs)):
        y = numpy.lcm(x,i)
        ys.append(y)
    return xs,ys

p = plotLCMinRange(12,120)
plt.plot(p[0],p[1],'ro')
plt.show()

def generatePossibleStringedEDOs(numStandardPerOctave,limit=121):
    #keys are edos
    #values are (numStandardPerOctave,other)
    edoFinestGrained = {}
    for i in range(1,limit):
        l = numpy.lcm(numStandardPerOctave,i)
        edoFinestGrained[l] = (numStandardPerOctave,i)
    return edoFinestGrained

if __name__ == "__main__":
    print(sorted(generatePossibleStringedEDOs(12)))


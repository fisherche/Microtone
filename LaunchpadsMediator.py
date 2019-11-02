from launchpadLayout import LaunchpadLayout
from launchpad import Launchpad
from abc import ABC
import mido

class Mediator(ABC):

    def transmit(self, origin, message):
        pass

class ConcreteMediator(Mediator):
    def __init__(self, layout):
        self.layout = layout
        self.controllerCount = 0 #holds number of controllers plus 1
        self.controllerLookupDict = dynamicSetAttr() #look up 

    def dynamicSetattr():
        count = 0
        for i in self.layout.objLst:
            attr = "controller" + str(count)
            setattr(self,attr,i) #set a controller number attribute for each in the layout
            attrMediator = attr + ".mediator"
            setattr(self,attrMediator,self) #set that controller's mediator to be this mediator
            count += 1
        self.controllerCount = count  
        return controllerLookupDict




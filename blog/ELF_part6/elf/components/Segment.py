from elf.Utils import *
from elf.components.headers.Ph import Ph

class Segment(object):

    def __init__(self, pType, pFlag, align = 0):
        self.sectionNameList = []
        self.pType = pType
        self.pFlag = pFlag
        self.align = align
    
    def appendSectionName(self, name):
        self.sectionNameList.append(name)

    def sectionNum(self):
        return len(self.sectionNameList)

    def getType(self):
        return self.pType

    def getFlag(self):
        return self.pFlag

    def getAlign(self):
        return self.align

    def getSectionName(self, key = None):
        if key == None:
            return self.sectionNameList
        else:
            return self.sectionNameList[key]

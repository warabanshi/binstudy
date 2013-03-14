
class Segment(object):

    def __init__(self, pType, pFlag):
        self.sectionList = []
        self.pType = pType
        self.pFlag = pFlag
    
    def appendSection(self, sec):
        self.sectionList.append(sec)

    def count(self):
        return len(self.sectionList)

    def getTyep(self):
        return self.pType

    def getFlag(self):
        return self.pFlag

    def getSection(self, index = None):
        if index == None:
            return self.sectionList
        else:
            return self.sectionList[index]

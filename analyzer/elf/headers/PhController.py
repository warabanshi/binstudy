from Ph import Ph

class PhController:

    def __init__(self, binList, eh):
        self.eh     = eh
        self.phList = []
        self.binList = binList

        self.aggregate(eh)

    def aggregate(self, eh):
        phSize = eh.get('ph_size')
        phOff  = eh.get('ph_offset')
        phNum  = eh.get('ph_num')

        for i in range(phNum):
            ph = Ph(self.binList)
            ph.retrieve(phOff + phSize * i)

            self.phList.append(ph)

    def setShNames(self, shList):
        for ph in self.phList:
            ph.setShNames(shList)

    def getPhList(self):
        return self.phList

    def getPh(self, key):
        return self.phList[key]

    def removePh(self, key):
        del self.phList[key]

    def getTotalSize(self):
        return self.eh.get('ph_size') * len(self.phList)

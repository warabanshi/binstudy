class PhController(object):

    def __init__(self):
        self.programList = []

    def append(self, p):
        self.programList.append(p)

    def getProgramList(self):
        return self.programList

    def setSection(self, sectionList):
        for p in self.programList:
            p.setSection(sectionList)

#    def removePh(self, key):
#        del self.phList[key]
#
#    def getTotalSize(self):
#        return self.eh.get('ph_size') * len(self.phList)
#
#    # set sh for ph that ph must including
#    def restructureAll(self, shCtrl):
#
#        ph = self.phList[0]
#        ph.set('offset', self.eh.get('eh_size'))
#        ph.set('filesize', self.eh.get('ph_size') * len(self.phList))
#        ph.set('memory_size', self.eh.get('ph_size') * len(self.phList))
#
#        offset = 64 # ELF header = 64byte
#
#        for ph in self.phList[1:]:  # index 0 is PHDR type
#            [ph.setSh(shCtrl.getSh(shName)) for shName in ph.getShNames()]
#            offset = ph.restructure(offset)

from Sh import Sh

class ShController:

    def __init__(self, binList, eh):
        self.shList = [] 
        self.eh     = eh
        self.binList = binList

        self.aggregate(eh)
        self.setShName(eh)
        self.setBody()

    def aggregate(self, eh):
        shSize = eh.get('sh_size')
        shOff  = eh.get('sh_offset')
        shNum  = eh.get('sh_num')

        for i in range(shNum):
            sh = Sh(self.binList)
            sh.retrieve(shOff + shSize * i)

            self.shList.append(sh)

    def getShList(self):
        return self.shList

    def getSh(self, key):
        if isinstance(key, basestring):
            return self.shList[self.snTab[key]]
        else:
            return self.shList[key]

    def setShName(self, eh):
        nameSec = self.getSh(eh.get('shstrndx'))

        offset = nameSec.get('offset')
        size = nameSec.get('size')
        snTab = {}

        sectionStr = ''.join(map(chr, nameSec.getRange(offset, size)))
        for (n, sh) in enumerate(self.shList):
            index = sh.get('name_index')
            s = sectionStr[index:]
            name = s[:s.find("\0")]
            sh.setName(name)
            snTab[name] = n

        self.snTab = snTab

    def setBody(self):
        for sh in self.shList:
            # if you try to get .bss division it will occur the error
            # since .bss division has no physical area size until execute
            sh.setBody(sh.getRange(sh.get('offset'), sh.get('size')))

from elf.Utils import *
from elf.components.headers.Sh import Sh
from elf.components.Section import Section

class ShController(object):

    def __init__(self):
        self.sectionList = []

    def append(self, section):
        self.sectionList.append(section)

    def getSectionList(self):
        return self.sectionList

    def getSection(self, key):
        if isinstance(key, basestring):
            key = self.searchSection(key)

        return self.sectionList[key]

    # return section index
    def searchSection(self, name):
        for (i, s) in enumerate(self.sectionList):
            if s.getName() == name:
                return i

        return None

    def makeShStr(self):
        nameList = [s.getName() for s in self.sectionList]
        nameStr = "\0".join(nameList) + "\0"

        return nameStr

    def setShStrTab(self, shStr):
        shStrTab = map(ord, shStr)

        for (i, s) in enumerate(self.sectionList):
            if s.getName() == '.shstrtab':
                s.setBodyList(shStrTab)
                return True

        # if .shstrtab isn't exits then make it
        shStrList = shStr.split("\0")

        shList = []
        shList += convLE(shStrList.index('.shstrtab'), 4)           # name_index
        shList += convLE(3, 4)                                      # type
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # flag
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # address
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # offset
        shList += convLE(len(shStr), 8)                             # size
        shList += [0x00, 0x00, 0x00, 0x00]                          # link
        shList += [0x00, 0x00, 0x00, 0x00]                          # info
        shList += convLE(1, 0)                                      # address_align
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # entry_table_size

        sh = Sh().retrieve(shList)
        self.sectionList.append(Section(shStrTab, '.shstrtab', sh))

    def resetNameIndex(self, shStr):
        shStrList = shStr.rstrip("\0").split("\0")

        for sName in shStrList:
            s = self.getSection(sName)
            idx = sum([len(name+"\0") for name in shStrList[:shStrList.index(sName)]])
            s.getSh().set('name_index', idx)

            # for debug
            #print('index = %3d, name = %s' % (idx, sName))

#    def removeSh(self, key):
#        if isinstance(key, basestring):
#            del self.shList[self.snTab[key]]
#            del self.snTab[key]
#        else:
#            raise('removeSh must receive key with sh_name')
#
#    def getTotalShSize(self):
#        return self.eh.get('sh_size') * len(self.shList)
#
#    def getTotalSectionSize(self):
#        return sum([len(sh.getBody()) for sh in self.shList])
#        #for sh in self.shList:
#        #    print(hex(len(sh.getBody())))
#
#    def getShStrIndex(self):
#        for (i, sh) in enumerate(self.shList):
#            if sh.getName() == '.shstrtab':
#                return int(i)

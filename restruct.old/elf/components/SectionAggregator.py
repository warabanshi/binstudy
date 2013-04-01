from elf.Utils import *
from elf.Relation import *
from elf.components.Section import Section
from elf.components.headers.Sh import Sh

class SectionAggregator(object):

    def __init__(self):
        self.sectionList = []

    def append(self, section):
        self.sectionList.append((section, section.getName()))

    def count(self):
        return len(self.sectionList)

    def dump(self):
        [sec.echo() for (sec, name) in self.sectionList]

    def find(self, needle):
        for (idx, (sec, name)) in enumerate(self.sectionList):
            if name == needle:
                return idx

    def remove(self, name):
        del(self.sectionList[self.find(name)])

    def get(self, key = None):
        if key == None:
            return self.sectionList

        if isinstance(key, int):
            return self.sectionList[key]
        else:
            idx = self.find(key)
            if idx == None:
                return None
            else:
                return self.get(idx)

    def resetOffset(self, phSize):
        prevEnd = phSize
        for s, name in self.sectionList:
            print('name: %s, offset: %s' % (name, hex(prevEnd)))
            s.getSh().set('offset', prevEnd)

            size = s.getSh().get('size')
            align = s.getSh().get('address_align')
            mod = size % align

            prevEnd += size
            if mod > 0:
                prevEnd += (align - mod)

        return prevEnd

    def makeShStrSection(self):
        shStr = "\0"
        for s, name in self.sectionList:
            sh = s.getSh()
            sh.set('name_index', len(shStr))
            shStr += s.getName() + "\0"

        shStrIdx = len(shStr)
        shStr += ".shstrtab\0"

        shStrTab = map(ord, shStr)

        shList = []
        shList += convLE(shStrIdx, 4)                               # name_index
        shList += convLE(3, 4)                                      # type
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # flag
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # address
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # offset(dummy)
        shList += convLE(len(shStr), 8)                             # size
        shList += [0x00, 0x00, 0x00, 0x00]                          # link
        shList += [0x00, 0x00, 0x00, 0x00]                          # info
        shList += convLE(1, 8)                                      # address_align
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # entry_table_size
 
        sh = Sh().retrieve(shList)
        self.append(Section(shStrTab, '.shstrtab', sh))

    def makeBody(self, headerSize):
        withOrder = [(sectionOrder.index(name), (sec, name)) for sec, name in self.sectionList]
        sortedSectionList = sorted(withOrder, key=lambda x: x[0])

        body = []
        secList = []
        for (order, (sec, name)) in sortedSectionList:
            sec.getSh().set('offset', headerSize + len(body))

            tmpBody = sec.getBody()
            align = sec.getSh().get('address_align')
            mod = len(tmpBody) % align
            if mod > 0:
                tmpBody += [0x00 for x in range(align - mod)]

            body += tmpBody
            secList.append((sec, name))

        self.sectionList = secList

        return body

from elf.Utils import *
from elf.components.headers.Sh import Sh
from elf.components.Section import Section

class SectionController(object):

    def __init__(self):
        self.sectionList = []

    def append(self, section):
        self.sectionList.append(section)

    def getSectionList(self):
        nullSh = Sh()
        nullSh.retrieve([0x00 for i in range(56)])
        nullSection = Section([], '', nullSh)

        strSection = self.makeShStrSection()

        return (nullSection, self.sectionList, strSection)

    def makeShStrSection(self):
        shStr = "\0"
        for s in self.sectionList:
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
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # offset
        shList += convLE(len(shStr), 8)                             # size
        shList += [0x00, 0x00, 0x00, 0x00]                          # link
        shList += [0x00, 0x00, 0x00, 0x00]                          # info
        shList += convLE(1, 0)                                      # address_align
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # entry_table_size

        sh = Sh().retrieve(shList)
        return Section(shStrTab, '.shstrtab', sh)


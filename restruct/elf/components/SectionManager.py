from elf.Utils import *
from elf.Relation import *
from elf.components.headers.Sh import Sh

class SectionManager(object):

    def __init__(self):
        self.sectionList = []

    def append(self, name, body, sh):
        self.sectionList.append({
            'name': name, 'body': body, 'sh': sh
        })

    def find(self, needle):
        for (idx, h) in enumerate(self.sectionList):
            if needle == h['name']:
                return idx

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

    def makeBody(self, headerSize):
        withOrder = [(sectionOrder.index(h['name']), h) for h in self.sectionList]
        sortedSectionList = sorted(withOrder, key=lambda x: x[0])

        body = []
        newSectionList = []
        for (order, h) in sortedSectionList:
            tmpBody = h['body']
            align = h['sh'].get('address_align')
            mod = (headerSize+len(body)) % align
            padding = 0

            if mod > 0:
                padding = align - mod
                tmpBody = [0x00 for x in range(align - mod)] + tmpBody

            if h['name'] == '.dynamic':
                padding += 2880
                tmpBody = [0x00 for x in range(2880)] + tmpBody

            h['sh'].set('offset', headerSize + len(body) + padding)
            body += tmpBody
            newSectionList.append(h)

        self.sectionList = newSectionList

        return body

    def resetAddress(self, org):
        for h in self.sectionList:
            attr = relationList.get(h['name'])
            if attr == None:
                continue

            if attr & SEC['ALLOC'] == 0:
                continue

            offset = h['sh'].get('offset')
            h['sh'].set('address', offset + org)

            if attr & SEC['READONLY'] == 0:
                h['sh'].set('address', offset + org + 0x200000)

    def makeShStrSection(self, offset):
        shStr = "\0"
        for h in self.sectionList:
            h['sh'].set('name_index', len(shStr))
            shStr += h['name'] + "\0"

        shStrIdx = len(shStr)
        shStr += ".shstrtab\0"

        shStrTab = map(ord, shStr)

        shList = []
        shList += convLE(shStrIdx, 4)                               # name_index
        shList += convLE(3, 4)                                      # type
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # flag
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # address
        shList += convLE(offset, 8)                                 # offset(dummy)
        shList += convLE(len(shStr), 8)                             # size
        shList += [0x00, 0x00, 0x00, 0x00]                          # link
        shList += [0x00, 0x00, 0x00, 0x00]                          # info
        shList += convLE(1, 8)                                      # address_align
        shList += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # entry_table_size
 
        sh = Sh().retrieve(shList)
        self.append('.shstrtab', shStrTab, sh)

        return shStrTab

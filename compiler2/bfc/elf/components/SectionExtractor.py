from elf.Utils import *
from elf.Relation import *
from elf.components.headers.Sh import Sh
from elf.components.headers.Eh import Eh

class SectionExtractor(object):

    def __init__(self, byteList):
        self.eh = Eh()
        self.eh.retrieve(byteList[0:64])

        self.byteList = byteList

    def extract(self):
        shSize  = self.eh.get('sh_size')
        shNum   = self.eh.get('sh_num')
        shOff   = self.eh.get('sh_offset')
        strTab  = self.retrieveStringTable()

        result = []
        for idx in range(1, shNum):

            if idx == self.eh.get('shstrndx'):
                continue

            shStart = shOff + shSize * idx

            sh = Sh()
            sh.retrieve(self.byteList[shStart:shStart+shSize])

            name = retrieveStr(strTab, sh.get('name_index'))
            body = self.byteList[sh.get('offset'):sh.get('offset')+sh.get('size')]

            if name == '.symtab' or name ==  '.strtab':
                continue

            result.append((name,  body,  sh))

        return result

    def retrieveStringTable(self):
        shSize  = self.eh.get('sh_size')
        shNum   = self.eh.get('sh_num')
        shOff   = self.eh.get('sh_offset')

        # get string table section header start position
        shStrStart  = shOff + shSize * self.eh.get('shstrndx')

        strSh = Sh()
        strSh.retrieve(self.byteList[shStrStart:shStrStart+shSize])

        strOff  = strSh.get('offset')
        strSize = strSh.get('size')
        strTab = ''.join(map(chr, self.byteList[strOff:strOff+strSize]))

        return strTab

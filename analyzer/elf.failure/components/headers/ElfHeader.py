from Header import Header
from elf.Utils import *

class ElfHeader(Header):

    org = 0x400000

    def getOrg(self):
        return self.org

    def retrieve(self, binList, offset = 0):
        self.setPos(offset)
        self.setBinList(binList)

        self.set('magic',      self.getMagic())
        self.set('type',       self.getWord())
        self.set('machine',    self.getWord())
        self.set('version',    self.getDw())
        self.set('entry_addr', self.getQw())
        self.set('ph_offset',  self.getQw('ph_offset'))
        self.set('sh_offset',  self.getQw('sh_offset'))
        self.set('flags',      self.getDw())
        self.set('eh_size',    self.getWord())
        self.set('ph_size',    self.getWord('ph_size'))
        self.set('ph_num',     self.getWord('ph_num'))
        self.set('sh_size',    self.getWord('sh_size'))
        self.set('sh_num',     self.getWord('sh_num'))
        self.set('shstrndx',   self.getWord('shstrndx'))

        self.clearBinList()

    def getMagic(self, isFetch = True):
        if isFetch:
            self.pos += 16
      
        return self.binList[0:16]

    def output(self):
        r = []
        r += self.get('magic')
        r += convLE(self.get('type'),       2)
        r += convLE(self.get('machine'),    2)
        r += convLE(self.get('version'),    4)
        r += convLE(self.get('entry_addr'), 8)
        r += convLE(self.get('ph_offset'),  8)
        r += convLE(self.get('sh_offset'),  8)
        r += convLE(self.get('flags'),      4)
        r += convLE(self.get('eh_size'),    2)
        r += convLE(self.get('ph_size'),    2)
        r += convLE(self.get('ph_num'),     2)
        r += convLE(self.get('sh_size'),    2)
        r += convLE(self.get('sh_num'),     2)
        r += convLE(self.get('shstrndx'),   2)

        return r

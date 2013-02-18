from Header import Header
from elf.Utils import *

class ElfHeader(Header):

    org = 0x400000

    def getOrg(self):
        return self.org

    def retrieve(self, binList, offset = 0):
        self.resetPos(offset)

        self.set('magic',      self.getMagic(binList))
        self.set('type',       self.getWord(binList))
        self.set('machine',    self.getWord(binList))
        self.set('version',    self.getDw(binList))
        self.set('entry_addr', self.getQw(binList))
        self.set('ph_offset',  self.getQw(binList))
        self.set('sh_offset',  self.getQw(binList))
        self.set('flags',      self.getDw(binList))
        self.set('eh_size',    self.getWord(binList))
        self.set('ph_size',    self.getWord(binList))
        self.set('ph_num',     self.getWord(binList))
        self.set('sh_size',    self.getWord(binList))
        self.set('sh_num',     self.getWord(binList))
        self.set('shstrndx',   self.getWord(binList))

    def getMagic(self, binList):
        self.resetPos(self.pos + 16)
        return binList[0:16]

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

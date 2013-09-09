from Header import Header
from bfc.elf.Utils import *

# ELF header
class Eh(Header):

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

    def echo(self):
        print('magic: %s'       % self.get('magic'))
        print('type: %s'        % self.get('type'))
        print('machine: %s'     % self.get('machine'))
        print('version: %s'     % self.get('version'))
        print('entry_addr: %s'  % self.get('entry_addr'))
        print('ph_offset: %s'   % self.get('ph_offset'))
        print('sh_offset: %s'   % self.get('sh_offset'))
        print('flags: %s'       % self.get('flags'))
        print('eh_size: %s'     % self.get('eh_size'))
        print('ph_size: %s'     % self.get('ph_size'))
        print('ph_num: %s'      % self.get('ph_num'))
        print('sh_size: %s'     % self.get('sh_size'))
        print('sh_num: %s'      % self.get('sh_num'))
        print('shstrndx: %s'    % self.get('shstrndx'))


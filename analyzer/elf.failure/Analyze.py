import sys, struct
from elf.header.ElfHeader import ElfHeader
from elf.header.ProgramHeader import ProgramHeader
from elf.header.SectionHeader import SectionHeader

class Analyze:

    pos = 0
    binList = []
    keyEntry = {}

    elfHeader = None
    shList = []       # section header list
    phList = []       # program header list
    snTab  = {}       # section name table

    def __init__(self, filename):
        f = open(filename)
        self.binList = map(lambda x: int(ord(x)), f.read())

        self.setEh()    #set elf header
        self.setPh()    #set program header
        self.setSh()    #set section header

        self.setSectionName()
        self.setSectionBody()

    # argument list expected in little endien
    def convBin(self, l):
        b = 0
        for byte in reversed(l):
            b = (b << 8) | byte

        return b

    # bs: bytesize
    def fetch(self, bs, key = None):
        r = self.convBin(self.binList[self.pos:self.pos+bs])
        self.pos += bs
        if key != None:
            self.keyEntry[key] = r

        return r

    def setPos(self, pos):
        self.pos = pos

    def getByte(self, key = None):
        return self.fetch(1, key)

    def getWord(self, key = None):
        return self.fetch(2, key)

    def getDw(self, key = None):
        return self.fetch(4, key)

    def getQw(self, key = None):
        return self.fetch(8, key)

    def getMagic(self, isFetch = True):
        if isFetch:
            self.pos += 16
      
        return '/'.join(map(hex, self.binList[0:16]))

    def getKeyEntry(self, key):
        return self.keyEntry[key]

    def getRange(self, start, size):
        return self.binList[start:start+size]

    def setEh(self):
        e = ElfHeader()
        e.set('magic',      self.getMagic())
        e.set('type',       self.getWord())
        e.set('machine',    self.getWord())
        e.set('version',    self.getDw())
        e.set('entry_addr', self.getQw())
        e.set('ph_offset',  self.getQw())
        e.set('sh_offset',  self.getQw('sh_offset'))
        e.set('flags',      self.getDw())
        e.set('eh_size',    self.getWord())
        e.set('ph_size',    self.getWord('ph_size'))
        e.set('ph_num',     self.getWord('ph_num'))
        e.set('sh_size',    self.getWord('sh_size'))
        e.set('sh_num',     self.getWord('sh_num'))
        e.set('strsec_idx', self.getWord('strsec_idx'))
        self.elfHeader = e

    def setPh(self):
        for i in range(self.getKeyEntry('ph_num')):
            p = ProgramHeader()
            p.set('segment_type',       self.getDw())
            p.set('permission_flag',    self.getDw())
            p.set('offset',             self.getQw())
            p.set('virtual_addr',       self.getQw())
            p.set('physical_addr',      self.getQw())
            p.set('filesize',           self.getQw())
            p.set('memory_size',        self.getQw())
            p.set('align',              self.getQw())

            self.phList.append(p)

    def setSh(self):
        self.setPos(self.getKeyEntry('sh_offset'))
        for i in range(0, self.getKeyEntry('sh_num')):
            s = SectionHeader()
            s.set('name_index',         self.getDw())
            s.set('type',               self.getDw())
            s.set('flag',               self.getQw())
            s.set('address',            self.getQw())
            s.set('offset',             self.getQw())
            s.set('size',               self.getQw())
            s.set('link',               self.getDw())
            s.set('info',               self.getDw())
            s.set('address_align',      self.getQw())
            s.set('entry_table_size',   self.getQw())

            self.shList.append(s)

    def setSectionName(self):
        nameSection = self.getSh(self.getKeyEntry('strsec_idx'))
        offset = nameSection.get('offset')
        size = nameSection.get('size')

        sectionStr = ''.join(map(chr, self.getRange(offset, size)))
        for (n, sh) in enumerate(self.shList):
            index = sh.get('name_index')
            s = sectionStr[index:]
            name = s[:s.find("\0")]
            sh.setName(name)
            self.snTab[name] = n

    def setSectionBody(self):
        for sh in self.shList:
            offset  = sh.get('offset')
            size    = sh.get('size')
            # if you try to get .bss division it will occur the error
            # since .bss division has no physical area size until execute
            sh.setBody(self.getRange(offset, size))

    def echoSn(self):
        print('-- section names ----------')
        for (sn, order) in sorted(self.snTab.items(), key=lambda x:x[1]):
            print('%3d : %20s' % (order, sn))

    def getEh(self):
        return self.elfHeader

    def getPh(self, key):
        return self.phList[key]

    def getSh(self, key):
        if isinstance(key, basestring):
            return self.shList[self.snTab[key]]
        else:
            return self.shList[key]


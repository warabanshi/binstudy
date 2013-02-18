import sys, struct
from elf.Utils import *
from elf.components.headers.ElfHeader import ElfHeader
from ctypes import *

class WriteElf:

    def __init__(self):
        self.sectionList = {}
        self.segmentList = {}
        self.startAddr = 0

    def setSection(self, sctNull, sctList, sctStr):
        self.sectionList['null'] = sctNull
        self.sectionList['list'] = sctList
        self.sectionList['str'] = sctStr

    def setSegment(self, segPhdr, segList):
        self.segmentList['phdr'] = segPhdr
        self.segmentList['list'] = segList

    def setStartAddr(self, startAddr):
        self.startAddr = startAddr

    def make(self):
        bodyLen = sum([len(s.bodyList) for s in self.segmentList['list']])
        shStrLen = len(self.sectionList['str'].getBodyList())
        shStrOff = 64 + 56 + 56 * len(self.segmentList['list']) + bodyLen
        shOff = shStrOff + shStrLen

        print(map(chr, self.sectionList['str'].getBodyList()))
        print("segment len: %d, body len: %d" % (len(self.segmentList['list']), bodyLen))

        eh = self.makeEhBase()
        eh.set('entry_addr', self.startAddr)
        eh.set('ph_offset', 64)
        eh.set('sh_offset', shOff)
        eh.set('ph_num', len(self.segmentList['list'])+1)
        eh.set('sh_num', len(self.sectionList['list'])+2)
        eh.set('shstrndx', len(self.sectionList['list'])+1)

        ph = self.segmentList['phdr'].getPh().output()
        body = []
        for seg in self.segmentList['list']:
            ph += seg.getPh().output()
            body += seg.getBodyList()

        sh = self.sectionList['null'].getSh().output()
        for sec in self.sectionList['list']:
            sh += sec.getSh().output()

        body += self.sectionList['str'].getBodyList()

        strSh = self.sectionList['str'].getSh()
        strSh.set('offset', shStrOff)
        sh += strSh.output()


        result = eh.output() + ph + body + sh
        p = (c_ubyte * len(result))()
        p[:] = result
        with open('write.out', 'wb') as fp:
            fp.write(p)

    # eh expects ElfHeader object
    def makeEhBase(self):

        eh = []
        eh += [0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01]            # magic
        eh += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] 
        eh += convLE(2, 2)                             # e_type (EXEC)
        eh += convLE(0x3e, 2)                          # e_machine (amd64)
        eh += convLE(1, 4)                             # e_version (1)
        eh += convLE(0, 8)                             # e_entry    (set later)
        eh += convLE(0, 8)                             # e_phoff    (set later)
        eh += convLE(0, 8)                             # e_shoff    (set later)
        eh += convLE(0, 4)                             # e_flags
        eh += convLE(64, 2)                            # e_ehsize (64)
        eh += convLE(56, 2)                            # e_phentsize (56)
        eh += convLE(0, 2)                             # e_phnum    (set later)
        eh += convLE(64, 2)                            # e_shentsize (64)
        eh += convLE(0, 2)                             # e_shnum    (set later)
        eh += convLE(0, 2)                             # e_shstrndx (set later)

        e = ElfHeader()
        e.retrieve(eh)

        return e

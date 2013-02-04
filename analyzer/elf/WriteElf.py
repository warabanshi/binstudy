import sys, struct
from ctypes import *

class WriteElf:

    org = 0x400000

    def __init__(self):
        self.phList = []
        self.shList = []

    def convLE(self, val, byteNum):
        le = []
        for i in range(byteNum):
            le.append((val >> i*8) & 0xff)

        return le

    def make(self):

        r = self.makeEh()

        p = (c_ubyte * len(r))()
        p[:] = r
        with open('write.out', 'wb') as fp:
            fp.write(p)


    # eh expects ElfHeader object
    def makeEh(self):

        shOff = 64 + (len(self.phList) * 56) + self.getSectionSize()

        eh = []
        eh += [0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01]            # magic
        eh += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] 
        eh += self.convLE(2, 2)                     # e_type (EXEC)
        eh += self.convLE(0x3e, 2)                  # e_machine (amd64)
        eh += self.convLE(1, 4)                     # e_version (1)
        eh += self.convLE(self.getEntryAddr(), 8)   # e_entry
        eh += self.convLE(56, 8)                    # e_phoff (eh and ph are contiguous)
        eh += self.convLE(shOff, 8)                 # e_shoff
        eh += self.convLE(0, 4)                     # e_flags
        eh += self.convLE(64, 2)                    # e_ehsize (64)
        eh += self.convLE(56, 2)                    # e_phentsize (56)
        eh += self.convLE(len(self.phList), 2)      # e_phnum
        eh += self.convLE(64, 2)                    # e_shentsize (64)
        eh += self.convLE(len(self.shList), 2)      # e_shnum
        eh += self.convLE(0, 2)                     # e_shstrndx (implement later)

        return eh

    def setPhList(self, ph):
        self.phList = ph

    def setSections(self, sh, is_strsec = None):
        self.shList.append(sh)

        if (is_strsec != None):
            self.eh[strsec_idx] = len(self.shList) - 1

    def getSectionSize(self):
        # implement later
        #return sum([len(shList[i].getBody()) for i in range(len(self.shList))])

        return 0 #dummy

    def getEntryAddr(self):
        # implement later
        #return self.org + self.sections.getEntryOffset()

        return 0 #dummy

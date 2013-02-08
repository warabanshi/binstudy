import sys, struct
from elf.Utils import *
from ctypes import *

class WriteElf:

    org = 0x400000

    def __init__(self, phCtrl, shCtrl):
        self.phCtrl = phCtrl
        self.shCtrl = shCtrl

    def make(self):
        # test chu
        #[s.echo() for s in self.shCtrl.getSectionList()]

        # restruct shstrtab
        shStr = self.shCtrl.makeShStr()
        self.shCtrl.setShStrTab(shStr)

        # recalcurate name_index
        self.shCtrl.resetNameIndex(shStr)

        # set section to program list
        self.phCtrl.setSection(self.shCtrl.getSectionList())

#        er = self.makeEh()
#        pr = self.makePh()
#        (sr, br) = self.makeSh()
#
#        result = er + pr + sr + br
#
#        p = (c_ubyte * len(result))()
#        p[:] = result
#        with open('write.out', 'wb') as fp:
#            fp.write(p)
#
#    def getSectionSize(self):
#        shList = self.shCtrl.getShList()
#        return sum([len(sh.getBody()) for sh in shList])
#
#    def getEntryAddr(self):
#        sh = self.shCtrl.getSh('.text')
#        return sh.get('address')
#
#    # eh expects ElfHeader object
#    def makeEh(self):
#
#        shOff = 64 + self.phCtrl.getTotalSize() + self.shCtrl.getTotalSectionSize()
#
#        eh = []
#        eh += [0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01]            # magic
#        eh += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] 
#        eh += self.convLE(2, 2)                     # e_type (EXEC)
#        eh += self.convLE(0x3e, 2)                  # e_machine (amd64)
#        eh += self.convLE(1, 4)                     # e_version (1)
#        eh += self.convLE(self.getEntryAddr(), 8)   # e_entry
#        eh += self.convLE(64, 8)                    # e_phoff (eh and ph are contiguous)
#        eh += self.convLE(shOff, 8)                 # e_shoff
#        eh += self.convLE(0, 4)                     # e_flags
#        eh += self.convLE(64, 2)                    # e_ehsize (64)
#        eh += self.convLE(56, 2)                    # e_phentsize (56)
#        eh += self.convLE(len(self.phCtrl.getPhList()), 2)  # e_phnum
#        eh += self.convLE(64, 2)                    # e_shentsize (64)
#        eh += self.convLE(len(self.shCtrl.getShList()), 2)  # e_shnum
#        eh += self.convLE(self.shCtrl.getShStrIndex(), 2)   # e_shstrndx (implement later)
#
#        return eh
#
#    def makePh(self):
#        self.phCtrl.restructure(self.shCtrl)
#
#        p = []
#        for ph in self.phCtrl.getPhList():
#            p += self.convLE(ph.get('segment_type'),    4)
#            p += self.convLE(ph.get('permission_flag'), 4)
#            p += self.convLE(ph.get('offset'),          8)
#            p += self.convLE(ph.get('virtual_addr'),    8)
#            p += self.convLE(ph.get('physical_addr'),   8)
#            p += self.convLE(ph.get('filesize'),        8)
#            p += self.convLE(ph.get('memory_size'),     8)
#            p += self.convLE(ph.get('align'),           8)
#
#        return p
#
#
#    def makeSh(self):
#        s = []
#        b = []
#        for sh in self.shCtrl.getShList():
#            s += self.convLE(sh.get('name_index'),      4)
#            s += self.convLE(sh.get('type'),            4)
#            s += self.convLE(sh.get('flag'),            8)
#            s += self.convLE(sh.get('address'),         8)
#            s += self.convLE(sh.get('offset'),          8)
#            s += self.convLE(sh.get('size'),            8)
#            s += self.convLE(sh.get('link'),            4)
#            s += self.convLE(sh.get('info'),            4)
#            s += self.convLE(sh.get('address_align'),   8)
#            s += self.convLE(sh.get('entry_table_size'),8)
#
#            b += sh.getBody()
#
#        return (s, b)

import sys, struct
from elf.Utils import *
from elf.components.headers.ElfHeader import ElfHeader
from ctypes import *

class WriteElf:

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

        eh = self.makeEhBase()
        eh = self.phCtrl.restructHeaders(eh)
        ph = self.phCtrl.outputPh()
        seg = self.phCtrl.outputSegment()
        seg += self.getShStrTab(self.shCtrl)
        eh = self.setShPart(eh, self.shCtrl)
        sh = [0x0 for i in range(64)]
        sh += self.phCtrl.outputSh()

        eh.set('sh_offset', len(eh.output() + ph + seg))
        eh.set('entry_addr', len(eh.output() + ph))

        result = eh.output() + ph + seg + sh
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

    def setShPart(self, eh, shCtrl):
        sList = shCtrl.getSectionList()
        for (i, s) in enumerate(sList):
            if s.getName() == '.shstrtab':
                eh.set('shstrndx', i)

        eh.set('sh_num', len(sList))
        eh.set('sh_size', 64)

        return eh

    def getShStrTab(self, shCtrl):
        for s in shCtrl.getSectionList():
            if s.getName() == '.shstrtab':
                return s.getBodyList()

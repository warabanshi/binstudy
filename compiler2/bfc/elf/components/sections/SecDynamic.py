import struct

from bfc.elf.components.headers.Sh import Sh
from Section import Section

class SecDynamic(Section):

    def makeSection(self):
        e = []
        e += self.makeDynamicSection(0x01, 0x01) # NEEDED
        e += self.makeDynamicSection(0x04, 0x00) # HASH
        e += self.makeDynamicSection(0x05, 0x00) # STRTAB
        e += self.makeDynamicSection(0x06, 0x00) # SYMTAB
        e += self.makeDynamicSection(0x0a, 0x00) # STRSZ
        e += self.makeDynamicSection(0x0b, 0x0b) # SYMENT
        e += self.makeDynamicSection(0x15, 0x00) # DEBUG
        e += self.makeDynamicSection(0x03, 0x00) # PLTGOT
        e += self.makeDynamicSection(0x02, 0x00) # PLTRELSZ
        e += self.makeDynamicSection(0x14, 0x00) # PLTREL
        e += self.makeDynamicSection(0x17, 0x00) # JMPREL
        e += self.makeDynamicSection(0x6ffffffe, 0x00) # VERNEED
        e += self.makeDynamicSection(0x6fffffff, 0x00) # VERNEEDNUM
        e += self.makeDynamicSection(0x6ffffff0, 0x00) # VERSYM
        e += self.makeDynamicSection(0x00, 0x00) # NULL

        return struct.pack(str(len(e))+'B', *e)
        
    def makeDynamicSection(self, tag, un):
        valList =  struct.unpack('8B', struct.pack('<Q', tag))
        valList += struct.unpack('8B', struct.pack('<Q', un))

        return valList

import struct

from bfc.elf.components.headers.Sh import Sh
from Section import Section

class SecDynstr(Section):

    def makeSection(self):
        s  = "\0"
        s += 'libc.so.6' + "\0"
        s += 'exit' + "\0"
        s += 'pubchar' + "\0"
        s += 'getchar' + "\0"
        s += 'GLIBC_2.2.5' + "\0"

        return s


from bfc.elf.components.headers.Sh import Sh
from Section import Section

class SecInterp(Section):

    def makeSection(self):
        return '/lib64/ld-linux-x86-64.so.2' + "\0"


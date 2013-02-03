import sys, struct
from ctypes import *

class WriteElf:

    def __init__(self):
        self.binList = []
        self.eh = None
        self.phList = []
        self.shList = []
        print('writeelf called')

    def convLE(self, l):
        b = 0
        for byte in reversed(l):
            b = (b << 8) | byte

        return b

    def make(self):
        # expecting implement ELF generator statements
        eh = []
        eh.extend(map(lambda x: int(x, 16), self.eh.get('magic').split('/')))
        eh.extend(self.eh.get('type'))

        r = eh

        p = (c_ubyte * len(r))()
        p[:] = r
        with open('write.out', 'wb') as fp:
            fp.write(p)


    # eh expects ElfHeader object
    def setEh(self, eh):
        self.eh = eh

    def appendPh(self, ph):
        self.phList.appned(ph)

    def appendSh(self, sh, is_strsec = None):
        self.shList.append(sh)

        if (is_strsec != None):
            self.eh[strsec_idx] = len(self.shList) - 1


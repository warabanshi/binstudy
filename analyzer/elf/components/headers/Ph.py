from Header import Header
from elf.Utils import *

class Ph(Header):

    def retrieve(self, binList, offset = 0):
        self.setPos(offset)
        self.setBinList(binList)

        self.set('segment_type',       self.getDw())
        self.set('permission_flag',    self.getDw())
        self.set('offset',             self.getQw())
        self.set('virtual_addr',       self.getQw())
        self.set('physical_addr',      self.getQw())
        self.set('filesize',           self.getQw())
        self.set('memory_size',        self.getQw())
        self.set('align',              self.getQw())

        self.clearBinList()

        return self

    def output(self):
        r = []
        r += convLE(self.get('segment_type'),       4)
        r += convLE(self.get('permission_flag'),    4)
        r += convLE(self.get('offset'),             8)
        r += convLE(self.get('virtual_addr'),       8)
        r += convLE(self.get('physical_addr'),      8)
        r += convLE(self.get('filesize'),           8)
        r += convLE(self.get('memory_size'),        8)
        r += convLE(self.get('align'),              8)

        return r

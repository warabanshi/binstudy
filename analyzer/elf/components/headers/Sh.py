from Header import Header
from elf.utils import *

class Sh(Header):

    def retrieve(self, binList, offset = 0):
        self.setPos(offset)
        self.setBinList(binList)

        self.set('name_index',         self.getDw())
        self.set('type',               self.getDw())
        self.set('flag',               self.getQw())
        self.set('address',            self.getQw())
        self.set('offset',             self.getQw())
        self.set('size',               self.getQw())
        self.set('link',               self.getDw())
        self.set('info',               self.getDw())
        self.set('address_align',      self.getQw())
        self.set('entry_table_size',   self.getQw())

        self.clearBinList()

        return self

    def output(self):
        r = []
        r += convLE(self.get('name_index'),         4)
        r += convLE(self.get('type'),               4)
        r += convLE(self.get('flag'),               8)
        r += convLE(self.get('address'),            8)
        r += convLE(self.get('offset'),             8)
        r += convLE(self.get('size'),               8)
        r += convLE(self.get('link'),               4)
        r += convLE(self.get('info'),               4)
        r += convLE(self.get('address_align'),      8)
        r += convLE(self.get('entry_table_size'),   8)

        return r

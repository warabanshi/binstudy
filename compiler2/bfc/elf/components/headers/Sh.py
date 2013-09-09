from Header import Header
from bfc.elf.Utils import *

# section header
class Sh(Header):

    def __init__(self):
        Header.__init__(self)
        self.contents = {
            'name_index'    : 0,
            'type'          : 0,
            'flag'          : 0,
            'address'       : 0,
            'offset'        : 0,
            'size'          : 0,
            'link'          : 0,
            'info'          : 0,
            'address_align' : 0,
            'entry_table_size': 0,
        }

    def retrieve(self, byteList, offset = 0):
        self.resetPos(offset)

        self.set('name_index',         self.getDw(byteList))
        self.set('type',               self.getDw(byteList))
        self.set('flag',               self.getQw(byteList))
        self.set('address',            self.getQw(byteList))
        self.set('offset',             self.getQw(byteList))
        self.set('size',               self.getQw(byteList))
        self.set('link',               self.getDw(byteList))
        self.set('info',               self.getDw(byteList))
        self.set('address_align',      self.getQw(byteList))
        self.set('entry_table_size',   self.getQw(byteList))

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

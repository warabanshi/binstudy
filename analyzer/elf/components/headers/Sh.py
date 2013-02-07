from Header import Header

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

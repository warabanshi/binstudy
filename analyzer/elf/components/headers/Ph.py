from Header import Header

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

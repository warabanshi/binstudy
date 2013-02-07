from Header import Header

class ElfHeader(Header):

    def retrieve(self, binList, offset = 0):
        self.setPos(offset)
        self.setBinList(binList)

        self.set('magic',      self.getMagic())
        self.set('type',       self.getWord())
        self.set('machine',    self.getWord())
        self.set('version',    self.getDw())
        self.set('entry_addr', self.getQw())
        self.set('ph_offset',  self.getQw('ph_offset'))
        self.set('sh_offset',  self.getQw('sh_offset'))
        self.set('flags',      self.getDw())
        self.set('eh_size',    self.getWord())
        self.set('ph_size',    self.getWord('ph_size'))
        self.set('ph_num',     self.getWord('ph_num'))
        self.set('sh_size',    self.getWord('sh_size'))
        self.set('sh_num',     self.getWord('sh_num'))
        self.set('shstrndx',   self.getWord('shstrndx'))

        self.clearBinList()

    def getMagic(self, isFetch = True):
        if isFetch:
            self.pos += 16
      
        return self.binList[0:16]


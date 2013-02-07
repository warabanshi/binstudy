from Header import Header

class Sh(Header):

    def retrieve(self, offset):
        self.setPos(offset)

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

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setBody(self, body):
        self.body = body

    def getBody(self):
        return self.body

    def restructure(self):
        self.set('size', len(self.body))

    # method for debug
    def echo(self):
        lm = lambda n: (n, hex(n))
        print('====== Section Header(%s) ======' % self.name)
        print('name_index:      %s' % self.get('name_index'))
        print('type:            %s' % self.get('type'))
        print('flag:            %s' % self.get('flag'))
        print('address:         %s(%s)' % lm(self.get('address')))
        print('offset:          %s(%s)' % lm(self.get('offset')))
        print('size:            %s(%s)' % lm(self.get('size')))
        print('link:            %s' % self.get('link'))
        print('info:            %s' % self.get('info'))
        print('address_align:   %s' % self.get('address_align'))
        print('entry_table_size:%s' % self.get('entry_table_size'))

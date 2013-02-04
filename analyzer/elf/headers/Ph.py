from Header import Header

class Ph(Header):

    def retrieve(self, offset):
        self.setPos(offset)

        self.set('segment_type',       self.getDw())
        self.set('permission_flag',    self.getDw())
        self.set('offset',             self.getQw())
        self.set('virtual_addr',       self.getQw())
        self.set('physical_addr',      self.getQw())
        self.set('filesize',           self.getQw())
        self.set('memory_size',        self.getQw())
        self.set('align',              self.getQw())

    def setShNames(self, shCtrl):
        self.shNameList = []
        for sh in shCtrl.getShList():
            if self.isIncludeSh(sh.get('address')):
                self.shNameList.append(sh.getName())

    def isIncludeSh(self, sStart):
        pStart = self.get('physical_addr')
        pSize = self.get('memory_size')

        return (pStart <= sStart and sStart < pStart + pSize)


    # for debug method
    def echo(self):
        print('********* Program Header ***********')
        print('segment_type:    %s' % self.get('segment_type'))
        print('permission_flag: %s' % self.get('permission_flag'))
        print('offset:          %s' % self.get('offset'))
        print('virtual_addr:    %s' % self.get('virtual_addr'))
        print('physical_addr:   %s' % self.get('physical_addr'))
        print('filesize:        %s' % self.get('filesize'))
        print('memory_size:     %s' % self.get('memory_size'))
        print('align:           %s' % self.get('align'))

        print('')
        print('%%% including section headers %%%')
        print(' '.join(self.shNameList))

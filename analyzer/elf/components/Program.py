class Program(object):

    def __init__(self, ph, shList = []):
        self.ph = ph

        if (len(shList) > 0):
            setSectionName(shList)


    def setSectionName(self, shList):
        None

    def setShNames(self, shList):
        self.shNameList = []
        for sh in shList:
            if self.isIncludeSh(sh.get('address')):
                self.shNameList.append(sh.getName())

    def getShNames(self):
        return self.shNameList

    def isIncludeSh(self, sStart):
        pStart = self.get('physical_addr')
        pSize = self.get('memory_size')

        return (pStart <= sStart and sStart < pStart + pSize)

    # for debug method
    def echo(self):
        print('********* Program Header ***********')
        print('segment_type:    %s' % self.ph.get('segment_type'))
        print('permission_flag: %s' % self.ph.get('permission_flag'))
        print('offset:          %s' % self.ph.get('offset'))
        print('virtual_addr:    %s' % self.ph.get('virtual_addr'))
        print('physical_addr:   %s' % self.ph.get('physical_addr'))
        print('filesize:        %s' % self.ph.get('filesize'))
        print('memory_size:     %s' % self.ph.get('memory_size'))
        print('align:           %s' % self.ph.get('align'))

        # implement later
        #print('')
        #print('%%% including section headers %%%')
        #print(' '.join(self.shNameList))
        #print('')

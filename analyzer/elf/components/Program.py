class Program(object):

    def __init__(self, ph, sList = []):
        self.ph     = ph
        self.sList  = []

        if (len(sList) > 0):
            self.setSection(sList)
            self.setSectionName(sList)

    def setSection(self, sList):
        for s in sList:
            sh = s.getSh()
            if self.isIncludeSh(sh.get('address')):
                self.sList.append(s)

    def setSectionName(self, sList):
        self.sNameList = []

        for s in sList:
            sh = s.getSh()
            if self.isIncludeSh(sh.get('address')):
                self.sNameList.append(s.getName())

    def getSectionNameList(self):
        return self.sNameList

    def isIncludeSh(self, sStart):
        pStart = self.ph.get('physical_addr')
        pSize = self.ph.get('memory_size')

        return (pStart <= sStart and sStart < pStart + pSize)

    # method for debug
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

        print('')
        print('%%% including section headers %%%')
        print(' '.join(self.sNameList))
        print('')

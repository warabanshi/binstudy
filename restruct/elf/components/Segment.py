from elf.components.headers.Ph import Ph

class Segment(object):

    def __init__(self, pType, pFlag, align = 0):
        self.sectionList = []
        self.pType = pType
        self.pFlag = pFlag
        self.ph = self.makeBasePh(pType, pFlag, align)
    
    def appendSection(self, sec):
        self.sectionList.append(sec)

    def count(self):
        return len(self.sectionList)

    def getPh(self):
        return self.ph

    def getType(self):
        return self.pType

    def getFlag(self):
        return self.pFlag

    def getSection(self, index = None):
        if index == None:
            return self.sectionList
        else:
            return self.sectionList[index]

    def getSectionByName(self, name):
        for sec in self.sectionList:
            if sec.getName() == name:
                return sec

    def getSize(self):
        return sum([s.getSh().get('size') for s in self.sectionList])

    def makeBasePh(self, pType, pFlag, align = 0):
        ph = Ph()
        ph.set('segment_type',      pType)
        ph.set('permission_flag',   pFlag)
        ph.set('offset',            0)      # dummy
        ph.set('virtual_addr',      0)      # dummy
        ph.set('physical_addr',     0)      # dummy
        ph.set('filesize',          0)      # dummy
        ph.set('memory_size',       0)      # dummy
        ph.set('align',             align)  # dummy

        return ph

    def echo(self):
        lm = lambda n: (n, hex(n))

        print('====== Segment(type=%d) ======' % self.pType)

        print('segment_type     %s' % self.ph.get('segment_type'))
        print('permission_flag: %s' % self.ph.get('permission_flag'))
        print('offset:          %s' % self.ph.get('offset'))
        print('virtual_addr:    %s(%s)' % lm(self.ph.get('virtual_addr')))
        print('physical_addr:   %s(%s)' % lm(self.ph.get('physical_addr')))
        print('filesize:        %s(%s)' % lm(self.ph.get('filesize')))
        print('memory_size:     %s' % self.ph.get('memory_size'))
        print('align:           %s' % self.ph.get('align'))

class SegmentController(object):

    loadAlign = 0x200000
    orgAddr   = 0x400000

    def __init__(self):
        None

    def makeSegment(self, sctList):

        # some segment making statements

        return sctList

#    def append(self, p):
#        self.segmentList.append(p)
#
#    def getSegmentList(self):
#        return self.segmentList
#
#    def setSection(self, sectionList):
#        for p in self.segmentList:
#            #print('test setSection')
#            p.setSection(sectionList)
#
#    def restructHeaders(self, eh):
#        for (pos, p) in enumerate(self.segmentList):
#            if p.getPh().get('segment_type') == 6:  # PT_PHDR == 6
#                eh = self.restructPhdr(p, pos, eh)
#            elif p.getPh().get('segment_type') == 1: # PT_LOAD == 1
#                self.restructLoad(p, eh)
#            else:
#                None
#
#        return eh
#
#    def restructPhdr(self, p, pos, eh):
#        phOff = len(eh.output())
#        phSize= 56
#        phNum = len(self.segmentList)
#
#        eh.set('ph_offset', phOff)
#        eh.set('ph_size',   phSize)
#        eh.set('ph_num',    phNum)
#
#        phdrOff = phOff + (phSize * pos)
#        p.getPh().set('offset', phdrOff)
#        p.getPh().set('virtual_addr',   eh.getOrg() + phdrOff)
#        p.getPh().set('physical_addr',  eh.getOrg() + phdrOff)
#        p.getPh().set('filesize',       phSize * phNum)
#        p.getPh().set('meomry_size',    phSize * phNum)
#        p.getPh().set('align',          8)
#
#        p.echo()
#
#        return eh
#
#    def restructLoad(self, p, eh):
#        if p.getPh().get('permission_flag') == 5:   # RX = 5
#            baseAddr = eh.getOrg()
#        else:                                       # RW = 6
#            baseAddr = eh.getOrg() + self.loadAlign
#
#        offset = 0
#        addr = baseAddr + offset
#
#        p.getPh().set('offset', 0)
#        p.getPh().set('virtual_addr',   addr)
#        p.getPh().set('physical_addr',  addr)
#        p.getPh().set('filesize',       p.getSegmentSize())
#        p.getPh().set('memory_size',    p.getSegmentSize())
#        p.getPh().set('align',          self.loadAlign)
#
#        p.restructSection(addr)
#
#    def getOrderedLoadSegment(self):
#        segments = [(i, p.getStartAddr()) for (i, p) in enumerate(self.segmentList)]
#        sortSegments = sorted(segments, key=lambda t: t[1])
#
#        result = []
#        for (index, addr) in sortSegments:
#            if self.segmentList[index].getPh().get('segment_type') == 1:
#                result.append(self.segmentList[index])
#
#        return result
#
#
#    def outputPh(self):
#        for p in self.segmentList:
#            result = []
#            result += p.getPh().output()
#
#        return result
#
#    def outputSegment(self):
#        segment = []
#
#        # output PHDR
#        phdr = []
#        for p in self.segmentList:
#            phdr += p.getPh().output()
#        
#        segment += phdr
#
#        # output LOAD
#        for seg in self.getOrderedLoadSegment():
#            segment += seg.getSegmentBody()
#
#        return segment
#
#    def outputSh(self):
#        r = []
#        for p in self.segmentList:
#            r.extend(p.outputSh())
#        
#        return r
#

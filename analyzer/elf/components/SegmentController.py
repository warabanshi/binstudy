import elf.Attributes
from elf.sectionOrder import getOrder
from elf.components.headers.Ph import Ph
from elf.components.Segment import Segment

class SegmentController(object):

    loadAlign = 0x200000
    orgAddr   = 0x400000

    def __init__(self):
        self.segmentList = []
        self.phSegment = None

    def makeSegment(self, sctList):
        segBaseTbl = {}
        for sct in sctList:
            name = sct.getName()
            try:
                segBaseTbl[sct.getSh().get('flag')].append((getOrder(name), sct))
            except:
                segBaseTbl[sct.getSh().get('flag')] = []
                segBaseTbl[sct.getSh().get('flag')].append((getOrder(name), sct))

        segTbl = {}
        for (flag, segList) in segBaseTbl.items():
            segTbl[flag] = sorted(segList, key=lambda x: x[0])

        offset = 64 + 56 + 56 * len(segTbl)     # EH + PHDR + PHs offset
        addr = self.orgAddr + offset
        phList = []

        for (flag, contentList) in segTbl.items():
            bodyList = []
            for (order, sct) in contentList:
                bodyList += sct.getBodyList()
                align = sct.getSh().get('address_align')

                # padding 0x00
                if len(sct.getBodyList()) % align > 0:
                    bodyList += [0x0 for x in range(align - len(sct.getBodyList()) % align)]

            ph = Ph()
            ph.set('segment_type',      elf.Attributes.getPhFlag(flag))     # implement later
            ph.set('permission_flag',   flag)
            ph.set('offset',            offset)
            ph.set('virtual_addr',      addr)     # implement later
            ph.set('physical_addr',     addr)     # implement later
            ph.set('filesize',          0)      # implement later
            ph.set('memory_size',       0)      # implement later
            ph.set('align',             0)      # implement later

            self.segmentList.append(Segment(ph, bodyList))
            phList.append(ph)

            offset += len(bodyList)
            addr += offset

        print(phList[0].output())
        # make PHDR
        self.setPhSegment(offset, addr, len(phList))


        return sctList

    def setPhSegment(self, offset, addr, phNum):
        None # implement later

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

from elf.Utils import *
from elf.Relation import *
from elf.components.Segment import Segment

class SegmentMaker(object):

    def __init__(self, secAggr):
        self.sectionAggregator = secAggr
        self.segmentList = {}

    def getSegmentList(self):
        return self.segmentList

    def getSegment(self, key):
        try:
            return self.segmentList[key]
        except:
            return None

    def getEntryAddr(self):
        for key, seg in self.segmentList.items():
            try:
                sec = seg.getSectionByName('.text')
                return sec.getSh().get('address')
            except:
                continue

    def getCount(self):
        return len(self.segmentList)

    def getSectionList(self):
        return self.sectionAggregator.get()

    def make(self):
        # make INTERP segment
        r = self.sectionAggregator.get('.interp')
        if r != None:
            interp, name = r

            # prepare PHDR segment
            phdrSeg = Segment(PT['PHDR'], PFs['RX'], 8)
            phdrSeg.appendSection(interp)

            # prepare INTERP segment
            interpSeg = Segment(PT['INTERP'], PFs['R'], 1)
            interpSeg.appendSection(interp)

            self.segmentList['PHDR'] = phdrSeg
            self.segmentList['INTERP'] = interpSeg

        # make LOAD segment
        loadRW = Segment(PT['LOAD'], PFs['RW'], 0x200000)
        loadRX = Segment(PT['LOAD'], PFs['RX'], 0x200000)
        for sec, name in self.sectionAggregator.get():
            attr = relationList.get(name)
            if attr == None:
                continue

            if attr & SEC['ALLOC'] == 0:
                continue

            if attr & SEC['READONLY'] == 0:
                loadRW.appendSection(sec)
            else:
                loadRX.appendSection(sec)

        self.segmentList['LOAD_RW'] = loadRW
        self.segmentList['LOAD_RX'] = loadRX

        # make DYNAMIC segment
        r = self.sectionAggregator.get('.dynamic')
        if r != None:
            dynamic, name = r
            if (dynamic.getSh().get('flag') & SEC['LOAD']) == 0:
                None
            else:
                dynamicSeg = Segment(PT['DYNAMIC'], PFs['RW'], 8)
                dynamicSeg.appendSection(dynamic)
                self.segmentList['DYNAMIC'] = dynamicSeg

        # make NOTE segment
        for sec, name in self.sectionAggregator.get():
            if sec.getSh().get('flag') & SEC['LOAD'] == 0 or name.find('.note') < 0:
                continue

            try:
                self.segmentList['NOTE'].appnedSection(sec)
            except KeyError:
                noteSeg = Segment(PT['NOTE'], PFs['R'], 4)
                noteSeg.appendSection(sec)
                self.segmentList['NOTE'] = noteSeg

        # make GNU_EH_FRAME segment
        r = self.sectionAggregator.get('.eh_frame_hdr')
        if r != None:
            ehFrame, name = r
            if ehFrame.getSh().get('flag') & SEC['LOAD'] != 0:
                ehSeg = Segment(PT['GNU_EH_FRAME'], PFs['R'], 4)
                ehSeg.appendSection(ehFrame)
                self.segmentList['GNU_EH_FRAME'] = ehSeg

        # make GNU_RELRO segment
        relroStart  = 0x600e98      # indicate GNU_RELRO vma range
        relroEnd    = 0x601000
        for key, segment in self.segmentList.items():
            if      segment.getType() == PT['LOAD'] \
                and segment.count() > 0 \
                and segment.getSection(0).getSh().get('address') >=  relroStart \
                and segment.getSection(0).getSh().get('address') <=  relroEnd:

                sec = segment.getSection(0)
                try:
                    self.segmentList['GNU_RELRO'].appendSection(sec)
                except:
                    seg = Segment(PT['GNU_RELRO'], PFs['R'], 1)
                    seg.appendSection(sec)
                    self.segmentList['GNU_RELRO'] = seg

        # debug
        #for key, seg in self.segmentList.items():
        #    print(key)
        #    for sec in seg.getSection():
        #        print(sec.getName())

    def setOffset(self):
        for key in orderList:
            try:
                seg = self.segmentList[key]
                if key == 'LOAD_RX':
                    seg.getPh().set('offset', 0)
                elif key == 'PHDR':
                    seg.getPh().set('offset', 0x40) # 0x40 is size of ELF header
                else:
                    minOff = min([s.getSh().get('offset') for s in seg.getSection()])
                    seg.getPh().set('offset', minOff)

                # debug
                #print(hex(seg.getPh().get('offset')))

            except:
                continue

    def setSize(self):
        for key in orderList:
            try:
                seg = self.segmentList[key]
                seg.getPh().set('filesize', seg.getSize())
                seg.getPh().set('memory_size', seg.getSize())

                # test
                if key == 'LOAD_RX':
                    seg.getPh().set('filesize', seg.getSize()+606)
                    seg.getPh().set('memory_size', seg.getSize()+606)

                # debug
                #seg.echo()
            except:
                continue

    def setAddr(self, org):

        rxChildList = segmentRelation['LOAD_RX']
        rwChildList = segmentRelation['LOAD_RW']

        for key in orderList:
            try:
                seg = self.segmentList[key]
                ph = seg.getPh()

                if key == 'LOAD_RX' or key in rxChildList:
                    ph.set('virtual_addr', org + ph.get('offset'))
                    ph.set('physical_addr', org + ph.get('offset'))
                elif key == 'LOAD_RW' or key in rwChildList:
                    base = org + 0x200000
                    ph.set('virtual_addr', base + ph.get('offset'))
                    ph.set('physical_addr', base + ph.get('offset'))
                else:
                    None

                # debug
                #seg.echo()
            except:
                continue

    def resetSection(self):
        # make shstrtbl
        self.sectionAggregator.makeShStrSection()
        endOfBody = self.sectionAggregator.resetOffset(self.getCount()*56 + 64)

        return endOfBody

from elf.Utils import *
from elf.Relation import *
from elf.components.Segment import Segment
from elf.components.headers.Ph import Ph

class SegmentManager(object):

    def __init__(self):
        self.segmentList = {}

    def getSegmentList(self):
        return self.segmentList

    def mapping(self, sectionManager):
        # make INTERP segment
        h = sectionManager.get('.interp')
        if h != None:

            # prepare PHDR segment
            phdrSeg = Segment(PT['PHDR'], PFs['RX'], 8)
            phdrSeg.appendSectionName(h['name'])

            # prepare INTERP segment
            interpSeg = Segment(PT['INTERP'], PFs['R'], 1)
            interpSeg.appendSectionName(h['name'])

            self.segmentList['PHDR'] = phdrSeg
            self.segmentList['INTERP'] = interpSeg

        # make LOAD segment
        loadRW = Segment(PT['LOAD'], PFs['RW'], 0x200000)
        loadRX = Segment(PT['LOAD'], PFs['RX'], 0x200000)
        for h in sectionManager.get():
            attr = relationList.get(h['name'])
            if attr == None:
                continue

            if attr & SEC['ALLOC'] == 0:
                continue

            if attr & SEC['READONLY'] == 0:
                loadRW.appendSectionName(h['name'])
            else:
                loadRX.appendSectionName(h['name'])

        self.segmentList['LOAD_RW'] = loadRW
        self.segmentList['LOAD_RX'] = loadRX

        # make DYNAMIC segment
        h = sectionManager.get('.dynamic')
        if h != None:
            if (h['sh'].get('flag') & SEC['LOAD']) == 0:
                None
            else:
                dynamicSeg = Segment(PT['DYNAMIC'], PFs['RW'], 8)
                dynamicSeg.appendSectionName(h['name'])
                self.segmentList['DYNAMIC'] = dynamicSeg

        # make NOTE segment
        for h in sectionManager.get():
            if h['sh'].get('flag') & SEC['LOAD'] == 0 or h['name'].find('.note') < 0:
                continue

            try:
                self.segmentList['NOTE'].appnedSectionName(h['name'])
            except KeyError:
                noteSeg = Segment(PT['NOTE'], PFs['R'], 4)
                noteSeg.appendSectionName(h['name'])
                self.segmentList['NOTE'] = noteSeg

        # make GNU_EH_FRAME segment
        h = sectionManager.get('.eh_frame_hdr')
        if h != None:
            if h['sh'].get('flag') & SEC['LOAD'] != 0:
                ehSeg = Segment(PT['GNU_EH_FRAME'], PFs['R'], 4)
                ehSeg.appendSectionName(h['name'])
                self.segmentList['GNU_EH_FRAME'] = ehSeg

        # make GNU_RELRO segment
        relroStart  = 0x600e98      # indicate GNU_RELRO vma range
        relroEnd    = 0x601000
        for key, segment in self.segmentList.items():
            if segment.getType() == PT['LOAD'] and segment.sectionNum() > 0:
                firstSecName = segment.getSectionName(0)
                h = sectionManager.get(firstSecName)
                firstAddr = h['sh'].get('address') 

                if firstAddr >= relroStart and firstAddr <= relroEnd:
                    secName = segment.getSectionName(0)
                    try:
                        self.segmentList['GNU_RELRO'].appendSectionName(secName)
                    except:
                        seg = Segment(PT['GNU_RELRO'], PFs['R'], 1)
                        seg.appendSectionName(secName)
                        self.segmentList['GNU_RELRO'] = seg

        # debug
        #for key, seg in self.segmentList.items():
        #    print("---- %s ----" % key)
        #    for secName in seg.getSectionName():
        #        print(secName)

    def makePh(self, sectionManager):
        phList = []
        for key, seg in self.segmentList.items():
            offset = self.getOffset(key, seg, sectionManager)

            ph = Ph()
            ph.set('segment_type', seg.getType())
            ph.set('permission_flag', seg.getFlag())
            ph.set('offset', offset)
            ph.set('virtual_addr', self.getAddr(key, offset))
            ph.set('physical_addr', self.getAddr(key, offset))
            ph.set('filesize', self.getSize(key, seg, sectionManager))
            ph.set('memory_size', self.getSize(key, seg, sectionManager))
            ph.set('align', seg.getAlign())

            phList.append(ph)

        return phList

    def getOffset(self, key, seg, secm):
        try:
            if key == 'LOAD_RX':
                return 0
            elif key == 'PHDR':
                return 0x40     # 0x40 is size of ELF header
            else:
                secList = [secm.get(name) for name in seg.getSectionName()]
                return min([h['sh'].get('offset') for h in secList])

        except BaseException, e:
            print(e)

    def getSize(self, key, seg, secm):
        try:
            return sum([len(h['body']) for h in [secm.get(name) for name in seg.getSectionName()]])

        except BaseException, e:
            print(e)

    def getAddr(self, key, offset):

        org = 0x400000

        rxChildList = segmentRelation['LOAD_RX']
        rwChildList = segmentRelation['LOAD_RW']

        try:
            if key == 'LOAD_RX' or key in rxChildList:
                return org + offset
            elif key == 'LOAD_RW' or key in rwChildList:
                base = org + 0x200000
                return base + offset
            else:
                None

        except BaseException, e:
            print(e)

from elf.Utils import *
from elf.Relation import *
from elf.components.Segment import Segment

class SegmentMaker(object):

    def __init__(self):
        self.segmentList = {}

    def getSegmentList(self):
        return self.segmentList

#    def getSegment(self, key):
#        try:
#            return self.segmentList[key]
#        except:
#            return None
#
#    def getEntryAddr(self):
#        for key, seg in self.segmentList.items():
#            try:
#                sec = seg.getSectionByName('.text')
#                return sec.getSh().get('address')
#            except:
#                continue
#
#    def getCount(self):
#        return len(self.segmentList)
#
#    def getSectionList(self):
#        return self.sectionAggregator.get()

    def make(self, sectionAggregator):
        # make INTERP segment
        r = sectionAggregator.get('.interp')
        if r != None:
            interp, name = r

            # prepare PHDR segment
            phdrSeg = Segment(PT['PHDR'], PFs['RX'], 8)
            phdrSeg.appendSectionName(interp.getName())

            # prepare INTERP segment
            interpSeg = Segment(PT['INTERP'], PFs['R'], 1)
            interpSeg.appendSectionName(interp.getName())

            self.segmentList['PHDR'] = phdrSeg
            self.segmentList['INTERP'] = interpSeg

        # make LOAD segment
        loadRW = Segment(PT['LOAD'], PFs['RW'], 0x200000)
        loadRX = Segment(PT['LOAD'], PFs['RX'], 0x200000)
        for sec, name in sectionAggregator.get():
            attr = relationList.get(name)
            if attr == None:
                continue

            if attr & SEC['ALLOC'] == 0:
                continue

            if attr & SEC['READONLY'] == 0:
                loadRW.appendSectionName(name)
            else:
                loadRX.appendSectionName(name)

        self.segmentList['LOAD_RW'] = loadRW
        self.segmentList['LOAD_RX'] = loadRX

        # make DYNAMIC segment
        r = sectionAggregator.get('.dynamic')
        if r != None:
            dynamic, name = r
            if (dynamic.getSh().get('flag') & SEC['LOAD']) == 0:
                None
            else:
                dynamicSeg = Segment(PT['DYNAMIC'], PFs['RW'], 8)
                dynamicSeg.appendSectionName(name)
                self.segmentList['DYNAMIC'] = dynamicSeg

        # make NOTE segment
        for sec, name in sectionAggregator.get():
            if sec.getSh().get('flag') & SEC['LOAD'] == 0 or name.find('.note') < 0:
                continue

            try:
                self.segmentList['NOTE'].appnedSectionName(sec)
            except KeyError:
                noteSeg = Segment(PT['NOTE'], PFs['R'], 4)
                noteSeg.appendSectionName(name)
                self.segmentList['NOTE'] = noteSeg

        # make GNU_EH_FRAME segment
        r = sectionAggregator.get('.eh_frame_hdr')
        if r != None:
            ehFrame, name = r
            if ehFrame.getSh().get('flag') & SEC['LOAD'] != 0:
                ehSeg = Segment(PT['GNU_EH_FRAME'], PFs['R'], 4)
                ehSeg.appendSectionName(name)
                self.segmentList['GNU_EH_FRAME'] = ehSeg

        # make GNU_RELRO segment
        relroStart  = 0x600e98      # indicate GNU_RELRO vma range
        relroEnd    = 0x601000
        for key, segment in self.segmentList.items():
            if segment.getType() == PT['LOAD'] and segment.sectionNum() > 0:
                firstSecName = segment.getSectionName(0)
                firstSec, secName = sectionAggregator.get(firstSecName)
                firstAddr = firstSec.getSh().get('address') 

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

    def makePh(self, sectionAggregator):
        None

    def setOffset(self, sectionAggregator):
        for key in orderList:
            #try:
                seg = self.segmentList[key]
                secList = [sectionAggregator.get(name) for name in seg.getSectionName()]

                if key == 'LOAD_RX':
                    seg.getPh().set('offset', 0)
                elif key == 'PHDR':
                    seg.getPh().set('offset', 0x40) # 0x40 is size of ELF header
                else:
                    minOff = min([s.getSh().get('offset') for s in secList])
                    seg.getPh().set('offset', minOff)

                # debug
                print(hex(seg.getPh().get('offset')))

            #except BaseException, e:
            #    print(e)
            #    continue

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

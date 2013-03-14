from elf.Utils import *
from elf.Relation import *
from elf.components.Segment import Segment

class SegmentMaker(object):

    def __init__(self, secAggr):
        self.sectionAggregator = secAggr
        self.segmentList = {}

    def make(self):
        # make INTERP segment
        r = self.sectionAggregator.get('.interp')
        if r != None:
            interp, name = r

            # prepare PHDR segment
            phdrSeg = Segment(PT['PHDR'], PFs['RX'])

            # prepare INTERP segment
            interpSeg = Segment(PT['INTERP'], PFs['R'])
            interpSeg.appendSection(interp)

            self.segmentList['PHDR'] = phdrSeg
            self.segmentList['INTERP'] = interpSeg

        # make LOAD segment
        loadRW = Segment(PT['LOAD'], PFs['RW'])
        loadRX = Segment(PT['LOAD'], PFs['RX'])
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
                self.segmentList['DYNAMIC'] = Segment(PT['DYNAMIC'], PFs['RW'])

        # make NOTE segment
        for sec, name in self.sectionAggregator.get():
            if sec.getSh().get('flag') & SEC['LOAD'] == 0 or name.find('.note') < 0:
                continue

            try:
                self.segmentList['NOTE'].appnedSection(sec)
            except KeyError:
                self.segmentList['NOTE'] = Segment(PT['NOTE'], PFs['R'])

        # make GNU_EH_FRAME segment
        r = self.sectionAggregator.get('.eh_frame_header')
        if r != None:
            ehFrame, name = r
            if ehFrame.getSh().get('flag') & SEC['LOAD'] != 0:
                self.segmentList['GNU_EH_FRAME']= Segment(PT['GNU_EH_FRAME'], PFs['R'])

        # make GNU_RELRO segment
        #for key, segment in self.segmentList.items():
        #    if      segment.getType() == PT['LOAD']
        #        and segment.count() > 0


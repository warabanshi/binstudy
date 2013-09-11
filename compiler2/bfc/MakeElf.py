from elf.components.SectionManager import SectionManager
from elf.components.SegmentManager import SegmentManager
from elf.components.headers.Eh import Eh

class MakeElf(object):

    def __init__(self, translator):
        secm = self.initSection(text)
        #segm = self.initSegment()

        self.secm = secm
        #self.segm = segm

    def initSection(self, text):
        secm = SectionManager(text)

        return secm

    def initSegment(self):
        segm = SegmentManager()
        
        return segm

    def linking(self, translator):
        None

    def execute(self):
        None


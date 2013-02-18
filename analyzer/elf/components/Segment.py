#from elf.Relations import shouldIntoProgram

class Segment(object):

    def __init__(self, ph, bodyList):
        self.ph         = ph
        self.bodyList   = bodyList

    def getPh(self):
        return self.ph

#    def getStartAddr(self):
#        return self.startAddr
#
#    def isLoadType(self):
#        return self.ph.get('segment_type') == 1     # LOAD = 1
#
#    def setSection(self, sList):
#        for s in sList:
#            pType   = self.ph.get('segment_type')
#            pFlags  = self.ph.get('permission_flag')
#            shType  = s.getSh().get('type')
#            shFlags = s.getSh().get('flag')
#
#            if shouldIntoProgram(pType, pFlags, shType, shFlags):
#                self.sectionList.append(s)
#
#    def getSegmentSize(self):
#        result = 0
#        for s in self.sectionList:
#            fs = s.getSh().get('size')
#            align = s.getSh().get('address_align')
#            result += fs + (align - (fs % align))
#
#        return result
#
#    def getSegmentBody(self):
#        result = []
#        for s in self.sectionList:
#            bodyLen = len(s.getBodyList())
#            align = s.getSh().get('address_align')
#            if bodyLen % align > 0:
#                padding = align - (bodyLen % align)
#            else:
#                padding = 0
#
#            result += s.getBodyList() + [0x0 for i in range(padding)]
#
#        return result
#
#
#    def restructSection(self, addr, offset = 0):
#
#        nextAddr = addr + offset
#        self.startAddr = nextAddr
#
#        for s in self.sectionList:
#            s.getSh().set('address', nextAddr)
#            s.getSh().set('offset', offset)
#
#            bodyLen = len(s.getBodyList())
#            align = s.getSh().get('address_align')
#            if bodyLen % align > 0:
#                size = bodyLen + (align - (bodyLen % align))
#            else:
#                size = bodyLen
#
#            s.getSh().set('size', size)
#            nextAddr += size
#            offset += size
#
#    def outputSh(self):
#        r = []
#        for s in self.sectionList:
#            r.extend(s.getSh().output())
#
#        return r
#
#    # method for debug
#    def echo(self):
#        lm = lambda n: (n, hex(n))
#
#        print('********* Program Header ***********')
#        print('segment_type:    %s' % self.ph.get('segment_type'))
#        print('permission_flag: %s' % self.ph.get('permission_flag'))
#        print('offset:          %s(%s)' % lm(self.ph.get('offset')))
#        print('virtual_addr:    %s(%s)' % lm(self.ph.get('virtual_addr')))
#        print('physical_addr:   %s(%s)' % lm(self.ph.get('physical_addr')))
#        print('filesize:        %s(%s)' % lm(self.ph.get('filesize')))
#        print('memory_size:     %s(%s)' % lm(self.ph.get('memory_size')))
#        print('align:           %s' % self.ph.get('align'))
#
#        #print('')
#        #print('%%% including section headers %%%')
#        #print(' '.join(self.sNameList))
#        #print('')

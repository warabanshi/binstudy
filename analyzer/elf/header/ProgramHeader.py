from Header import Header

class ProgramHeader(Header):

    def setIncludeSection(self, sections):
        sectionNameList = []
        for section in sections:
            if self.isIncludeSection(section.get('address')):
                sectionNameList.append(section.getName())

    def isIncludeSection(self, sStart):
        pStart = self.get('physical_addr')
        pSize = self.get('memory_size')

        return (pStart <= sStart and sStart < pStart + pSize)

'''
    def echo(self):
        print('********* Program Header ***********')
        print('segment_type:    %s' % self.get('segment_type'))
        print('permission_flag: %s' % self.get('permission_flag'))
        print('offset:          %s' % self.get('offset'))
        print('virtual_addr:    %s' % self.get('virtual_addr'))
        print('physical_addr:   %s' % self.get('physical_addr'))
        print('filesize:        %s' % self.get('filesize'))
        print('memory_size:     %s' % self.get('memory_size'))
        print('align:           %s' % self.get('align'))
'''

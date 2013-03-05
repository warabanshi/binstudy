
class SectionAggregator(object):

    def __init__(self):
        self.sectionList = []

    def append(self, section):
        self.sectionList.append(section)

    def count(self):
        return len(self.sectionList)

    def dump(self):
        for sec in self.sectionList:
            sec.echo()

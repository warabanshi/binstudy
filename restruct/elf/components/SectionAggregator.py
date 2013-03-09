
class SectionAggregator(object):

    def __init__(self):
        self.sectionList = []
        self.nameList = []

    def append(self, section):
        self.sectionList.append((section, section.getName()))

    def count(self):
        return len(self.sectionList)

    def dump(self):
        [sec.echo() for (sec, name) in self.sectionList]

    def find(self, needle):
        for (idx, (sec, name)) in enumerate(self.sectionList):
            if name == needle:
                return idx

    def remove(self, name):
        del(self.sectionList[self.find(name)])

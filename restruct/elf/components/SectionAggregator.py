
class SectionAggregator(object):

    def __init__(self):
        self.sectionList = []

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

    def get(self, key = None):
        if key == None:
            return self.sectionList

        if isinstance(key, int):
            return self.sectionList[key]
        else:
            idx = self.find(key)
            if idx == None:
                return None
            else:
                return self.get(idx)

class Section(object):

    def __init__(self, bodyList, name, sh):
        self.bodyList = bodyList
        self.shName = name
        self.sh = sh

    def getBodyList(self):
        return self.bodyList

    def getShName(self):
        return self.shName

    def getSh(self):
        return self.sh

    # method for debug
    def echo(self):
        lm = lambda n: (n, hex(n))

        try:
            print('====== Section Header(%s) ======' % self.shName)
        except AttributeError:
            print('====== Section Header(no name setting) ====')

        print('name_index:      %s' % self.sh.get('name_index'))
        print('type:            %s' % self.sh.get('type'))
        print('flag:            %s' % self.sh.get('flag'))
        print('address:         %s(%s)' % lm(self.sh.get('address')))
        print('offset:          %s(%s)' % lm(self.sh.get('offset')))
        print('size:            %s(%s)' % lm(self.sh.get('size')))
        print('link:            %s' % self.sh.get('link'))
        print('info:            %s' % self.sh.get('info'))
        print('address_align:   %s' % self.sh.get('address_align'))
        print('entry_table_size:%s' % self.sh.get('entry_table_size'))

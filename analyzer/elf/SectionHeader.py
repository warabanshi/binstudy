from Header import Header

class SectionHeader(Header):

    def echo(self):
        print('============= Section Header ==========')
        print('name_index:      %s' % self.get('name_index'))
        print('type:            %s' % self.get('type'))
        print('flag:            %s' % self.get('flag'))
        print('address:         %s' % self.get('address'))
        print('offset:          %s' % self.get('offset'))
        print('size:            %s' % self.get('size'))
        print('link:            %s' % self.get('link'))
        print('info:            %s' % self.get('info'))
        print('address_align:   %s' % self.get('address_align'))
        print('entry_table_size:%s' % self.get('entry_table_size'))

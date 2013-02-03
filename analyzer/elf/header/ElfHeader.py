from Header import Header

class ElfHeader(Header):
    
    def echo(self):
        print('++++++++++ ELF Header +++++++++++')
        print('magic:       %s' % self.get('magic'))
        print('type:        %s' % self.get('type'))
        print('machine:     %s' % self.get('machine'))
        print('version:     %s' % self.get('version'))
        print('entry_addr:  %s' % self.get('entry_addr'))
        print('ph_offset:   %s' % self.get('ph_offset'))
        print('sh_offset:   %s' % self.get('sh_offset'))
        print('flags:       %s' % self.get('flags'))
        print('eh_size:     %s' % self.get('eh_size'))
        print('ph_size:     %s' % self.get('ph_size'))
        print('ph_num:      %s' % self.get('ph_num'))
        print('sh_size:     %s' % self.get('sh_size'))
        print('sh_num:      %s' % self.get('sh_num'))
        print('strsec_idx:  %s' % self.get('strsec_idx'))

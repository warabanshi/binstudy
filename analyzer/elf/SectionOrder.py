sectionOrder = (
    '.interp', '.note.gnu.build-id', '.hash', '.gnu.hash',
    '.dynsym', '.dynstr', '.gnu.hash', '.dynsym', '.dynstr',
    '.gnu.version', '.gnu.version_d', '.gnu.version_r', '.rela.init',
    '.rela.text', '.rela.fini', '.rela.rodata', '.rela.data.rel.ro',
    '.rela.data', '.rela.tdata', '.rela.tbss', '.rela.ctors',
    '.rela.dtors', '.rela.got', '.rela.bss', '.rela.ldata',
    '.rela.lbss', '.rela.lrodata', '.rela.ifunc', '.rela.plt',
    '.init', '.plt', '.text', '.fini', '.rodata', '.rodata1',
    '.eh_frame_hdr', '.eh_frame', '.gcc_except_table', '.eh_frame',
    '.gcc_except_table', '.tdata', '.tbss', '.preinit_array',
    '.init_array', '.fini_array', '.ctors', '.dtors',
    '.jcr', '.data.rel.ro', '.dynamic', '.got',
    '.got.plt', '.data', '.data1', '.bss', '.lbss',
    '.lrodata', '.ldata', '.stab', '.stabstr',
    '.stab.excl', '.stab.exclstr', '.stab.index', '.stab.indexstr',
    '.comment', '.debug', '.line', '.debug_srcinfo', '.debug_sfnames',
    '.debug_aranges', '.debug_pubnames', '.debug_info', '.debug_abbrev',
    '.debug_line', '.debug_frame', '.debug_str', '.debug_loc',
    '.debug_macinfo', '.debug_weaknames', '.debug_funcnames',
    '.debug_typenames', '.debug_varnames', '.debug_pubtypes',
    '.debug_ranges', '.gnu.attributes',
)

def getOrder(name):
    return sectionOrder.index(name)

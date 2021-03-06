# proggram haeder type
PT = {
    'NULL'      : 0,
    'LOAD'      : 1,
    'DYNAMIC'   : 2,
    'INTERP'    : 3,
    'NOTE'      : 4,
    'SHLIB'     : 5,
    'PHDR'      : 6,
    'TLS'       : 7,
    'NUM'       : 8,
    'LOOS'      : 0x60000000,
    'GNU_EH_FRAME' : 0x6474e550,
    'GNU_STACK' : 0x6474e551,
    'GNU_RELRO' : 0x6474e552,
    'LOSUNW'    : 0x6ffffffa,
    'SUNWBSS'   : 0x6ffffffa,
    'SUNWSTACK' : 0x6ffffffb,
    'HISUNW'    : 0x6fffffff,
    'HIOS'      : 0x6fffffff,
    'LOPROC'    : 0x70000000,
    'HIPROC'    : 0x7fffffff,
}

# program header flag
PF = {
    'X'         : (1 << 0),
    'W'         : (1 << 1),
    'R'         : (1 << 2),
    'MASKOS'    : 0x0ff00000,
    'MASKPROC'  : 0xf0000000,
}

PFs = {
    'X'         : PF['X'],
    'W'         : PF['W'],
    'R'         : PF['R'],
    'RW'        : PF['R'] | PF['W'],
    'RX'        : PF['R'] | PF['X'],
    'RWX'       : PF['R'] | PF['W'] | PF['X'],
}

# section header type
SHT = {
    'NULL'          : 0,
    'PROGBITS'      : 1,
    'SYMTAB'        : 2,
    'STRTAB'        : 3,
    'RELA'          : 4,
    'HASH'          : 5,
    'DYNAMIC'       : 6,
    'NOTE'          : 7,
    'NOBITS'        : 8,
    'REL'           : 9,
    'SHLIB'         : 10,
    'DYNSYM'        : 11,
    'INIT_ARRAY'    : 14,
    'FINI_ARRAY'    : 15,
    'PREINIT_ARRAY' : 16,
    'GROUP'         : 17,
    'SYMTAB_SHNDX'  : 18,
    'NUM'           : 19,
    'LOOS'          : 0x60000000,
    'GNU_ATTRIBUTES': 0x6ffffff5,
    'GNU_HASH'      : 0x6ffffff6,
    'GNU_LIBLIST'   : 0x6ffffff7,
    'CHECKSUM'      : 0x6ffffff8,
    'LOSUNW'        : 0x6ffffffa,
    'SUNW_move'     : 0x6ffffffa,
    'SUNW_COMDAT'   : 0x6ffffffb,
    'SUNW_syminfo'  : 0x6ffffffc,
    'GNU_verdef'    : 0x6ffffffd,
    'GNU_verneed'   : 0x6ffffffe,
    'GNU_versym'    : 0x6fffffff,
    'HISUNW'        : 0x6fffffff,
    'HIOS'          : 0x6fffffff,
    'LOPROC'        : 0x70000000,
    'HIPROC'        : 0x7fffffff,
    'LOUSER'        : 0x80000000,
    'HIUSER'        : 0x8fffffff,
}        

# section header flag
SHF = {
    'WRITE'     : (1 << 0),
    'ALLOC'     : (1 << 1),
    'EXECINSTR' : (1 << 2),
    'MERGE'     : (1 << 4),
    'STRINGS'   : (1 << 5),
    'INFO_LINK' : (1 << 6),
    'LINK_ORDER': (1 << 7),
    'OS_NONCONFORMING'  : (1 << 8),
    'GROUP'     : (1 << 9),
    'TLS'       : (1 << 10),
    'MASKOS'    : 0x0ff00000,
    'MASKPROC'  : 0xf0000000,
    'ORDERED'   : (1 << 30),
    'EXCLUDE'   : (1 << 31),
}

SHFs = {
    'A'     : SHF['ALLOC'],
    'W'     : SHF['WRITE'],
    'X'     : SHF['EXECINSTR'],
    'AW'    : SHF['ALLOC'] | SHF['WRITE'],
    'AX'    : SHF['ALLOC'] | SHF['EXECINSTR'],
    'AWX'   : SHF['ALLOC'] | SHF['WRITE'] | SHF['EXECINSTR'],
}

SEC = {
    'NO_FLAGS' :    0x000,
    'ALLOC' :       0x001,
    'LOAD' :        0x002,
    'RELOC' :       0x004,
    'READONLY' :    0x008,
    'CODE' :        0x010,
    'DATA' :        0x020,
    'ROM' :         0x040,
    'CONSTRUCTOR' : 0x080,
    'HAS_CONTENTS': 0x100,
    'NEVER_LOAD':   0x200,
    'THREAD_LOCAL': 0x400,
    'HAS_GOT_REF':  0x800,
    'IS_COMMON':    0x1000,
    'DEBUGGING':    0x2000,
    'IN_MEMORY':    0x4000,
    'EXCLUDE':      0x8000,
    'SORT_ENTRIES': 0x10000,
    'LINK_ONCE':    0x20000,
    'LINK_DUPLICATES':          0xc0000,
    'LINK_DUPLICATES_DISCARD':  0x0,
    'LINK_DUPLICATES_ONE_ONLY': 0x40000,
    'LINK_DUPLICATES_SAME_SIZE':0x80000,
    #'LINK_DUPLICATES_SAME_CONTENTS':    '\',
    'LINKER_CREATED':           0x100000,
    'KEEP':         0x200000,
    'SMALL_DATA':   0x400000,
    'MERGE':        0x800000,
    'STRINGS':      0x1000000,
    'GROUP':        0x2000000,
    'COFF_SHARED_LIBRARY':  0x4000000,
    'ELF_REVERSE_COPY':     0x4000000,
    'COFF_SHARED':  0x8000000,
    'TIC54X_BLOCK': 0x10000000,
    'TIC54X_CLINK': 0x20000000,
    'COFF_NOREAD':  0x40000000,
}

relationList = {
    '.text':   (SEC['HAS_CONTENTS'] | SEC['ALLOC'] | SEC['LOAD'] | SEC['READONLY'] | SEC['CODE']),
    '.rodata': (SEC['HAS_CONTENTS'] | SEC['ALLOC'] | SEC['LOAD'] | SEC['READONLY'] | SEC['DATA']),
    '.data':   (SEC['HAS_CONTENTS'] | SEC['ALLOC'] | SEC['LOAD'] | SEC['DATA']),
    '.bss':    (SEC['ALLOC']),
    '.interp': (SEC['HAS_CONTENTS'] | SEC['ALLOC'] | SEC['LOAD'] | SEC['READONLY'] | SEC['DATA']),
    '.sdata':  (SEC['HAS_CONTENTS'] | SEC['ALLOC'] | SEC['LOAD'] | SEC['DATA'] | SEC['SMALL_DATA']),
    '.comment':(SEC['HAS_CONTENTS']),

    '.note':               (SEC['ALLOC'] | SEC['READONLY']),
    '.note.gnu.build-id':  (SEC['ALLOC'] | SEC['READONLY']),
    '.hash':       (SEC['ALLOC'] | SEC['READONLY']),
    '.gnu.hash':   (SEC['ALLOC'] | SEC['READONLY']),
    '.dynsym':     (SEC['ALLOC'] | SEC['READONLY']),
    '.dynstr':     (SEC['ALLOC'] | SEC['READONLY']),
    '.gnu.version':(SEC['ALLOC'] | SEC['READONLY']),
    '.gnu.version_r':  (SEC['ALLOC'] | SEC['READONLY']),
    '.rela.plt':   (SEC['ALLOC'] | SEC['READONLY']),
    '.plt':        (SEC['ALLOC'] | SEC['READONLY']),
    '.dynamic':    (SEC['ALLOC'] | SEC['LOAD'] | SEC['HAS_CONTENTS'] | SEC['IN_MEMORY'] | SEC['LINKER_CREATED']),
    '.got.plt':    (SEC['ALLOC'] | SEC['LOAD'] | SEC['HAS_CONTENTS'] | SEC['IN_MEMORY'] | SEC['LINKER_CREATED']),
}

orderList = [
    'PHDR', 'INTERP', 'LOAD_RX', 'LOAD_RW', 'DYNAMIC',
    'NOTE', 'GNU_EH_FRAME', 'GNU_RELRO',
]

segmentRelation = {
    'LOAD_RX':  [
        'PHDR', 'INTERP', 'NOTE', 'GNU_EH_FRAME',
    ],
    'LOAD_RW':  [
        'DYNAMIC', 'GNU_RELRO',
    ]
}

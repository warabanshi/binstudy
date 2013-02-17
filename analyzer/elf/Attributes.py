pType = {
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

pFlag = {
    'X'         : (1 << 0),
    'W'         : (1 << 1),
    'R'         : (1 << 2),
    'MASKOS'    : 0x0ff00000,
    'MASKPROC'  : 0xf0000000,
}

pFlags = {
    'X'         : pFlag['X'],
    'W'         : pFlag['W'],
    'R'         : pFlag['R'],
    'RW'        : pFlag['R'] | pFlag['W'],
    'RX'        : pFlag['R'] | pFlag['X'],
    'RWX'       : pFlag['R'] | pFlag['W'] | pFlag['X'],
}

shType = {
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

shFlag = {
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

shFlags = {
    'A'     : shFlag['ALLOC'],
    'W'     : shFlag['WRITE'],
    'X'     : shFlag['EXECINSTR'],
    'AW'    : shFlag['ALLOC'] | shFlag['WRITE'],
    'AX'    : shFlag['ALLOC'] | shFlag['EXECINSTR'],
    'AWX'   : shFlag['ALLOC'] | shFlag['WRITE'] | shFlag['EXECINSTR'],
}

def getPhFlag(flag):
    try:
        return pFlag[pFlag.index(flag)]
    except:
        return None

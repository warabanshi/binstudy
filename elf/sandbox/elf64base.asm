BITS 64
    org     0x08048000

ehdr:                                   ; ELF64_Ehdr
            db  0x7f, "ELF", 2, 1, 1    ; e_ident
    times 9 db  0                       ; e_ident
            dw  1                       ; u16 e_type
            dw  0x3e                    ; u16 e_machine /usr/include/linux/elf-em.h
                                        ; 62 = x86-64
            dd  0x01                    ; u32 e_version
            dq  _start                  ; u64 e_entry
            dq  phdr - $$               ; u64 e_phoff
            dq  0x40                    ; u64 e_shoff
            dd  0                       ; u32 e_flags
            dw  ehdrsize                ; u16 e_ehsize
            dw  phdrsize                ; u16 e_phentisize
            dw  0                       ; u16 e_phnum
            dw  0x40                    ; u16 e_shentsize
            dw  0x05                    ; u16 e_shnum
            dw  0x02                    ; u16 e_shstrndx

ehdrsize    equ     $ - ehdr

phdr:                                   ; ELF64_Phdr
            dd                          ; u32 p_type
            dd                          ; u32 p_flags
            dq                          ; u64 p_offset
            dq                          ; u64 p_vaddr
            dq                          ; u64 p_paddr
            dq  filesize                ; u64 p_filesz
            dq  filesize                ; u64 p_memsz
            dq                          ; u64 p_align

phdrsize    equ     $ - phdr

_start:

; entry my program

filesize    equ     $ - $$

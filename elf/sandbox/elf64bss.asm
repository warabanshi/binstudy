BITS 64
    org     0x08048000

ehdr:                                   ; ELF64_Ehdr(ELF header)
            db  0x7f, "ELF", 2, 1, 1    ; e_ident
    times 9 db  0                       ; e_ident
            dw  2                       ; u16 e_type
            dw  0x3e                    ; u16 e_machine /usr/include/linux/elf-em.h
                                        ; 62 = x86-64
            dd  0x01                    ; u32 e_version
            dq  _start                  ; u64 e_entry
            dq  phdr - $$               ; u64 e_phoff
            dq  shdr - $$               ; u64 e_shoff
            dd  0                       ; u32 e_flags
            dw  ehdrsize                ; u16 e_ehsize
            dw  phdrsize                ; u16 e_phentisize
            dw  1                       ; u16 e_phnum
            dw  0x40                    ; u16 e_shentsize
            dw  3                       ; u16 e_shnum
            dw  1                       ; u16 e_shstrndx

ehdrsize    equ     $ - ehdr

phdr:                                   ; ELF64_Phdr(program header)
            dd  1                       ; u32 p_type
            dd  0x05                    ; u32 p_flags
            dq  0                       ; u64 p_offset
            dq  $$                      ; u64 p_vaddr
            dq  $$                      ; u64 p_paddr
            dq  filesize                ; u64 p_filesz
            dq  filesize                ; u64 p_memsz
            dq  0x1000                  ; u64 p_align

phdrsize    equ     $ - phdr

_start:
            mov     rax, 1
            mov     edx, 1
            mov     rsi, 0x08048001     ; 2nd argument have to pointer to string
                                        ; use E of magic number 'ELF'
            mov     edi, 1
            syscall

            mov     eax, 60
            mov     edi, 42
            syscall

shstrtbl:
            db  0
_text:
            db  ".text", 0      ; string must end with null byte
_shstrtbl:
            db  ".shstrtbl", 0  ; string must end with null byte
_bss:
            db  ".bss", 0

; declarations are specified in /usr/include/linux/elf.h
shdr:
            ; the first entry in the section header table (with an index 0)
            ; is reserved. and must contain all zeros.
            dd  0       ; u32 sh_name
            dd  0       ; u32 sh_type
            dq  0       ; u64 sh_flags
            dq  0       ; u64 sh_addr
            dq  0       ; u64 sh_offset
            dq  0       ; u64 sh_size
            dd  0       ; u32 sh_link
            dd  0       ; u32 sh_info
            dq  0       ; u64 sh_addralign
            dq  0       ; u64 sh_entsize
            
            ; section header for string table division
            ; this is specified to string table by ELF header of e_shstrndx
            dd  _shstrtbl - shstrtbl; u32 sh_name   index of string table section from
                                    ;               shstrtbl
            dd  3                   ; u32 sh_type       3 means SHT_STRTAB
            dq  0                   ; u64 sh_flags
            dq  0                   ; u64 sh_addr  this isn't appear in process memory
                                    ;               so this specifies 0
            dq  shstrtbl - $$       ; u64 sh_offset
            dq  shdr - shstrtbl     ; u64 sh_size
            dd  0                   ; u32 sh_link
            dd  0                   ; u32 sh_info
            dq  1                   ; u64 sh_addralign
            dq  0                   ; u64 sh_entsize

            ; section header for program division
            dd  _text - shstrtbl    ; u32 sh_name       section name index
            dd  1                   ; u32 sh_type       1 means SHT_PROGBITS
            dq  6                   ; u64 sh_flags      6 = SHF_ALLOC & SHF_ExEcINSTR
            dq  _start              ; u64 sh_addr       
            dq  _start - $$         ; u64 sh_offset
            dq  shstrtbl - _start   ; u64 sh_size
            dd  0                   ; u32 sh_link
            dd  0                   ; u32 sh_info
            dq  4                   ; u64 sh_addralign
            dq  0                   ; u64 sh_entsize

            ; section header for bss division
            dd  _bss - shstrtbl     ; u32 sh_name       section name index
            dd  8                   ; u32 sh_type       8 means SHT_NOBITS
            dq  3                   ; u64 sh_flags      3 = SHF_WRITE & SHF_ALLOC
            dq         ; u64 sh_addr  this isn't appear in process memory
                                    ;               so this specifies 0
            dq              ; u64 sh_offset
            dq  30000               ; u64 sh_size
            dd  0                   ; u32 sh_link
            dd  0                   ; u32 sh_info
            dq  16                  ; u64 sh_addralign
            dq  0                   ; u64 sh_entsize

filesize    equ     $ - $$

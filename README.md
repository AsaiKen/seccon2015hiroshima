Overview
--------
Writeups of SECCON2015 qualifying round in Hiroshima (I'm 1st.)

Contest URL
--------
http://seccon2015.connpass.com/event/21015/

Comment
--------
I solved 14 of 38 problems during the contest (3 hours).

I wrote exploits in the following steps.

1. understand ABI by reading objdump's outputs of binaries and lib-xxx-elf.S files in cross-20130826.tgz.
2. write '\x0A'-less shellcodes while reading instruction set manuals.
3. get offsets of BOF and stack addresses by using gdb or simulator.
4. write exploits with "HOT BLOOD".



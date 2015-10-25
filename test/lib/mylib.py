import struct
import telnetlib
import hexdump
import socket
import time


def p(data):
    return struct.pack('<I', data)


def pb(data):
    return struct.pack('>I', data)


def p16(data):
    return struct.pack('<H', data)


def p16b(data):
    return struct.pack('>H', data)


def u(data):
    return struct.unpack('<I', data)[0]


def shell(s):
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()


def xxd(data):
    hexdump.hexdump(data)


def mysock(ip, port):
    s = socket.create_connection((ip, port))
    return s


def zzz(t):
    time.sleep(t)


open('/tmp/senddata', mode='wb').write('')


def sl(s, data):
    s.send(data)
    log_f = open('/tmp/senddata', mode='ab')
    log_f.write(data)


def l(data):
    log_f = open('/tmp/senddata', mode='ab')
    log_f.write(data)

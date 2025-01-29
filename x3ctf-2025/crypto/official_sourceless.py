#!/usr/bin/env python

# x3CTF 2025
# Sourceless-Crypto: https://github.com/x3ctf/challenges-2025/tree/main/crypto/sourceless-crypto

"""
Official solution
"""

# Ookami
# Hackers Fight Club

# IMPORTS
from pwn import remote
from argparse import ArgumentParser
from string import printable

# Parser configuration
parser = ArgumentParser(description="Solución al reto Sourceless-Crypto de x3CTF 2025")
parser.add_argument("host", type=str, help="Dominio del host objetivo")
parser.add_argument("puerto", type=int, help="Puerto del host que aloja el reto")
parser.add_argument("-v", dest='verbosity', action='store_true')

# Parse Arguments
args = parser.parse_args()

#
# Starts connection
#
r = remote(args.host,args.puerto,ssl=True)

# Receive flag
r.sendlineafter(b'Operation: ',b'1')
encrypted_flag = r.recvline() 

# Send all printable chars and receive encrypted chars
r.sendlineafter(b'Operation: ',b'2')
r.sendlineafter(b'plaintext: ', printable.encode())
encrypted_printable = r.recvline()

# Finalize connection
r.close()
print()

# Format received data
encrypted_flag = eval(encrypted_flag.replace(b'Flag: ',b''))
encrypted_printable = eval(encrypted_printable.replace(b'Encrypted plaintext: ',b''))

# Variables
denonced_flag=b''
denonced_printable=b''

# Initialize nonce
nonce=0

# Undo the nonce XOR for the flag
for c in encrypted_flag:
    denonced_flag += (c ^ nonce).to_bytes(1)
    nonce += 1

# Undo the nonce XOR por printable chars
for c in encrypted_printable:
    denonced_printable += (c ^ nonce).to_bytes(1)
    nonce+=1

dictionary={chr(e):c for c,e in zip(printable,denonced_printable)}

# Print information
if args.verbosity:
    print('Created dictionary (Encrypted:Decrypted): ')
    print(dictionary)
    print()
print(f'Retrieved encrypted flag: {encrypted_flag}')
print()
print(f'Removed nonce flag: {denonced_flag}')
print()

# Decrypt flag with dictionary
flag=''
for c in denonced_flag:
    flag += dictionary[chr(c)]

print(f'Decrypted flag: {flag}')

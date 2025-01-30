#!/usr/bin/env python

# x3CTF 2025
# Sourceless-Crypto: https://github.com/x3ctf/challenges-2025/tree/main/crypto/sourceless-crypto

"""
My Solution
"""

# ------------------
# Ookami
# Hackers Fight Club
# ------------------

# IMPORTS
from pwn import xor

# Retrieved encrypted flag
encrypted_flag = b"\\F^itur%) /,B,'|0_p2pvd5emxyRo}wAD\x03m\x04\x05RPf\x00\x0b\x0b\rc\x0c\x0e\x19\x19\x17C\x14\x17\x1fEM\x1bV"

# Rechognized pattern
pattern=['1','0','3','2','5','4','7','6','9','8','b','a','d','c','f','e']

# Key array creation
key=[]
for first in pattern:
    for last in pattern:
       key.append(int(f'{first}{last}',16))

# Output flag
print(f'Decrypted Flag: {xor(encrypted_flag,key[:len(encrypted_flag)]).decode()}')

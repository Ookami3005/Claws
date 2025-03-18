#!/usr/bin/env python3

import random
import time

from pwn import remote,context
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('host',help='Host objetivo')
parser.add_argument('port',help='Puerto objetivo')

args = parser.parse_args()

context.log_level = 'error'

def get_random(length,seed):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    print(f'Seed: {seed}')
    random.seed(seed)  # seeding with current time 
    s = ""
    for _ in range(length):
        s += random.choice(alphabet)
    print(f'Token: {s}')
    return s

def try_seed(host,port):
    r = remote(host, port)
    seed = int(time.time()*1000)
    r.recvline()
    r.recvline()
    r.recvline()
    for i in range(50):
        token = get_random(20,seed+i)
        r.sendlineafter(b'exit):',token.encode())
        response = r.recvline()
        print(response)
        if b'Sorry' not in response:
            print()
            print(f'Flag: {r.recvline().decode()}')
            exit()
    r.close()


def main():

    for _ in range(1000):
        try_seed(args.host,args.port)
    
    
if __name__ == "__main__":
    main()

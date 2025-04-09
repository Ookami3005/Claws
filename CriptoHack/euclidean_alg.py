#!/usr/bin/env python

# ------------------
# Ookami
# Hackers Fight Club
# ------------------

from argparse import ArgumentParser

# Argument Parser Configuration
parser = ArgumentParser()
parser.add_argument('a', type=int, help='First integer')
parser.add_argument('b', type=int, help='Second integer')
args = parser.parse_args()

# Variable declaration
first = args.a if args.a > args.b else args.b
second = args.a if first != args.a else args.b

# Sequence generation
while second != 0:
    var = second
    second = first % second
    first = var

# Output GCD
print(first)

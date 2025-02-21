#!/usr/bin/env python

from argparse import ArgumentParser

# Parser configuration
parser = ArgumentParser(description="Extended Euclide's Algorithm implementation")
parser.add_argument('a', type=int, help='First integer')
parser.add_argument('b', type=int, help='Second integer')
parser.add_argument('-r','--result',type=int, dest='result', help='number to equal equation')
args = parser.parse_args()

# Variable declaration
greater = args.a if args.a > args.b else args.b
lesser = args.a if greater != args.a else args.b
first = greater
second = lesser

p,q = [],[]
it = 0

# Sequence generation
while second != 0:
    q.append(first // second)
    var = second
    second = first % second
    first = var

    if it == 0 or it == 1:
        p.append(it)
    else:
        p.append((p[it-2]-p[it-1]*q[it-2]) % greater)
    it+=1


p.append((p[it-2]-p[it-1]*q[it-2]) % greater)
coef1 = p.pop()
coef2 = (lesser * coef1 - 1) // greater

print(-coef2,coef1)

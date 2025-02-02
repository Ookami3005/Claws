#!/usr/bin/env python

# x3CTF 2025
# Pickle-Season: https://github.com/x3ctf/challenges-2025/tree/main/rev/pickle-season

"""
Solution
"""

# ---------------------------
# Ookami y Princesita (Dalix)
# Hackers Fight Club
# ---------------------------

# Dictionary keys to access
keys=[735, 674, 716, 764, 655, 699, 648, 763, 676, 663, 763, 656, 755, 706, 658, 717, 675, 658, 717, 672, 656, 756, 711, 693, 645, 711, 700, 753, 679, 746]

# Flag recreation
flag=''
for i in range(len(keys)-1,0,-1):
    flag += chr(keys[i] ^ keys[i-1])

# Output flag
print(flag)

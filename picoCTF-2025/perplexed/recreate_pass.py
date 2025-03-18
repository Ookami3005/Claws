#!/usr/bin/env python3

# ------------------
# Ookami
# Hackers Fight Club
# ------------------

# Binary representation of expected bytes: e1a71ef875237b61b99dfc5a5bdf69d2fe1bedf4ed67f4
string = list('1110000110100111000111101111100001110101001000110111101101100001101110011001110111111100010110100101101111011111011010011101001011111110000110111110110111110100111011010110011111110100')

index_to_insert = len(range(0,len(string),8))
for i in range(0,len(string)+index_to_insert,8):
    string.insert(i,'0')

string = string[:len(string)-2]

flag_binary = ''.join(string)

flag=''
for i in range(0,len(flag_binary),8):
    flag += chr(int(flag_binary[i:i+8],2))

print(flag)

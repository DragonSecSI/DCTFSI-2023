from pwn import *
from SECRET import flag, key

ct = xor(flag, key).hex()

print(ct)
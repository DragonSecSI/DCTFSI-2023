from pwn import *

# generate
key = b"MyKey"
flag = b"DCTF{Im_like_an_XOR_gate_I_cant_even}"

ct = xor(flag, key).hex()
print(ct)

# solv
ct = unhex(ct)
key = xor(ct, "DCTF{".encode()).decode()
pt = xor(ct, key[:5].encode())
print(pt)
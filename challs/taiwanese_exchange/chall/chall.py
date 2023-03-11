from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import hashlib
import os

FLAG = b"DCTF{...}"

p = 143615497288443699278657741405790299892568306256965415627539052409825836017353657422702954887012421128156715930710656724643496066965112661841047260515619652426136695978001210002967868458570937898831022362786629609366060795073931661831039571412758044831838455017076308366510393677279193818496361999301988488529
g = 2

print(f"p = {p}")
print(f"g = {g}")

a = bytes_to_long(os.urandom(64))
A = pow(g, a, p)
print(f"A = {A}")

b = bytes_to_long(os.urandom(128))
B = pow(g, b, p)
print(f"B = {B}")

shared = pow(g, a*b, p)
sha1 = hashlib.sha1()
sha1.update(long_to_bytes(shared))
key = sha1.digest()[:16]
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(FLAG, 16))
print(f"iv = {iv.hex()}")
print(f"ct = {ciphertext.hex()}")

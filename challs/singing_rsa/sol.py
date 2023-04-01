#from app.app import *
from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse

#context.log_level = 'debug'

r = remote("localhost", 1337)

MARKOV_PODPIS = b'To je poslal Marko.'


def sign(sporocilo: bytes):
    r.clean_and_log()
    r.recvuntil(b"Izbira: ", timeout=0.2)
    r.sendline(b"1")
    r.recvuntil(b": ")
    r.sendline(sporocilo)
    parts = r.recvuntil(b"\n\n").decode('utf-8').strip().split("\n")
    print(parts)
    _, podpis, e, n = parts
    podpis = int(podpis.split("=")[1])
    e = int(e.split("=")[1])
    n = int(n.split("=")[1])
    return podpis, e, n


_,  e, n = sign(b"a")  # Get public key

m = bytes_to_long(MARKOV_PODPIS)
print(f"Target {m=}")

a = 3
for a in range(3, 100):
    m_ = (m * pow(a, e, n)) % n
    m_bytes = long_to_bytes(m_)
    if any([x in m_bytes for x in [b"\x0a", b"\x00"]]):
        continue
    break

print(f"{a=}")
print(f"{m_=}")

signature_, _, _ = sign(m_bytes)
print(signature_)

signature = (signature_ * inverse(a, n)) % n
print(signature)

r.recvuntil(b"Izbira: ")
r.sendline(b"2")
r.sendline(MARKOV_PODPIS)
r.sendline(str(signature).encode())
r.sendline(b"3")
print(r.recvall().decode())

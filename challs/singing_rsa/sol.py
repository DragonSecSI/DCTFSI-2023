from app.app import *


s = CryptoSession()

n, e = s.get_public_key()

a = 11
x = bytes_to_long(MARKOV_PODPIS)
print(f"Target {x=}")

x_ = (bytes_to_long(MARKOV_PODPIS) * pow(a, e, n)) % n
print(f"{x_=}")

signature_, err = s.sign_message(long_to_bytes(x_))
print(signature_, err)

signature = (signature_ * inverse(a, n)) % n
print(signature)

print(s.get_flag(MARKOV_PODPIS, signature))

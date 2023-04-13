#!/usr/bin/env python3

import re
import os
import random
import subprocess

def main():
    flag = open("flag.txt", encoding="utf-8").read().strip()
    key = random.randbytes(len(flag))

    print("%-20.20s%s" % ("Flag:", flag))
    print("%-20.20s%s" % ("Flag hex:", flag.encode().hex()))
    print("%-20.20s%s" % ("Key:", key.hex()))
    flag_enc = encrypt_flag(pt=flag, key=key)
    print("%-20.20s%s" % ("Encrypted:", flag_enc.hex()))
    flag_dec = decrypt_flag(flag_enc, key)
    print("%-20.20s%s" % ("Decrypted:", flag_dec))
    assert flag == flag_dec

    assembly = open("shellcode.s", encoding="utf-8").read()
    flag_checker = ""
    for i in range(len(flag_enc)):
        flag_checker += \
f"""
    mov rsi, {flag_enc[i]}
    xor rsi, {key[i]}
    movzx r8, byte [rdi]
    sub rsi, r8
    or rax, rsi
    add rdi, 1
"""

    assembly = re.sub(r'; <flag check>', flag_checker, assembly)
    open("shellcode_compile.s", "w", encoding="utf-8").write(assembly)
    subprocess.run(["nasm", "-f", "bin", "shellcode_compile.s", "-o", "shellcode"]).check_returncode()
    shellcode = open("shellcode", "rb").read()
    c_prog = open("main.c", encoding="utf-8").read()
    c_prog = re.sub(r'"<shellcode>"', to_c_byte_array(shellcode), c_prog)
    open("main_compile.c", "w", encoding="utf-8").write(c_prog)
    subprocess.run(["gcc", "-s", "main_compile.c", "-O2", "-o", "baby_rev_2"]).check_returncode()
    os.remove("shellcode_compile.s")
    os.remove("shellcode")
    os.remove("main_compile.c")

def encrypt_flag(pt: str, key: bytes) -> bytes:
    pt = pt.encode("utf-8")
    flag_enc = []

    for i in reversed(range(len(pt))):    
        flag_enc.append(pt[i] ^ key[i])

    return bytes(reversed(flag_enc))

def decrypt_flag(ct: bytes, key: bytes) -> str:
    flag_dec = []

    for i in reversed(range(len(ct))):
        flag_dec.append(ct[i] ^ key[i])

    return bytes(reversed(flag_dec)).decode("utf-8")

def to_c_byte_array(x: bytes) -> str:
    return "{ 0x" + x.hex(',').replace(',', ', 0x') + " }"

if __name__ == "__main__":
    main()

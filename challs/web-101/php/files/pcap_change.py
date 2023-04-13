import re
import os
import sys

packet_sample = r"00000001235600000001234508004500001d0001([0-9A-F]{2})004011[0-9A-F]{20}654d2e510009[0-9A-F]{4}([0-9A-F]{2})".upper(
)
pattern = re.compile(packet_sample, re.IGNORECASE)

assert len(sys.argv) in (
    2, 3), "Usage: python3 pcap_change.py <input.pcap> [<output.pcap>]"

READMODE = len(sys.argv) == 2
filename = sys.argv[1]

with open(filename, "rb") as f:
    data = f.read()

hex_data = data.hex().upper()

out = hex_data[:]


def to_l33t_case(s):
    return s.lower().replace("a", "4").replace("e", "3").replace("i", "1").replace("o", "0").replace("s", "5").replace("t", "7")


def packet_visible(match):
    return (int(match.group(1), 16) & 0x80) == 0


def packet_character(match):
    return chr(int(match.group(2), 16))


if not READMODE:
    current_no = len([1 for m in re.finditer(
        pattern, hex_data) if packet_visible(m)])
    to_inject = os.environ['FLAG2']
    assert len(to_inject) <= current_no

    print(len(to_inject), to_inject)


def process_byte(match):
    global to_inject
    global out

    if packet_visible(match):
        if READMODE:
            print(packet_character(match), end="")
            return
        _start = match.start()
        _end = match.end()
        curr = match.group(0)
        #print(len(curr), curr)
        if len(to_inject) == 0:
            curr = curr[:40] + "80" + curr[42:]
        else:
            chr_byte = ord(to_inject[0]).to_bytes(1, "big").hex()
            to_inject = to_inject[1:]
            curr = curr[:-2] + chr_byte
        # print(curr)
        out = out[:_start] + curr + out[_end:]


for match in re.finditer(pattern, hex_data):
    process_byte(match)
print()
if len(sys.argv) == 2:
    exit(0)
outfile = sys.argv[2]
rebuilt = bytes.fromhex(out)
with open(outfile, "wb") as f:
    f.write(rebuilt)

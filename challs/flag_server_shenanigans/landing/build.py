import sys
from hashlib import md5
from os import environ
import re

TARGET_COORDS = environ["WIFI_COORDS"]
P1_COORDS = "46.05009035948195 N 14.468951516050701 E"

HTML_FMT = """<div><code{extra}>{coord}</code> <b><code>&deg{side}</code></b></div>"""
DIGITS_FMT = "%.6f"


def process(coords):
    m = re.findall(r"(\d+\.\d*)\s*([NSWE])", coords)
    assert len(m) == 2
    x1, xw = m[0]
    y1, yw = m[1]
    print(x1, xw, y1, yw)
    assert xw in "NS"
    assert yw in "EW"
    x1, y1 = [DIGITS_FMT % float(t) for t in (x1, y1)]
    return [(x1, xw), (y1, yw)]


def fmt_html(pcoords, extra=""):
    return '\n'.join([
        HTML_FMT.format(coord=x, side=y, extra=extra) for x, y in pcoords
    ])


P1_COORDS = fmt_html(process(P1_COORDS))

TARGET_COORDS = process(TARGET_COORDS)

# hash the target coords
TARGET_COORDS = [(md5(x.encode('ascii')).digest().hex(), y)
                 for x, y in TARGET_COORDS]

TARGET_COORDS = fmt_html(TARGET_COORDS, extra=" typ=\"md5\"")

with open("preset.html", "r") as f:
    webpage = f.read()


def replace_marker(s, mstr, repl):
    return re.sub(r"\{%%\s*%s\s*%%\}" % mstr, repl, s)


webpage = replace_marker(webpage, "p1coords", P1_COORDS)
webpage = replace_marker(webpage, "targetcoords", TARGET_COORDS)

with open("index.html", "w") as f:
    f.write(webpage)

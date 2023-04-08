#!/bin/bash

set -eux

if [ ! -f rockyou.txt ]; then
    echo "[~] Downloading rockyou.txt"
    wget "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt" -O rockyou.txt
fi


echo "[~] Decrypting"
pdfcrack -f ./evil_doc_enc.pdf -w rockyou.txt -o ./evil_doc_dec.pdf

echo "[~] Done"

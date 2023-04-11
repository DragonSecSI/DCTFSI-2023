#!/bin/bash

set -eux

PASS="!!cherry!!"

qpdf --encrypt $PASS $PASS 128 --use-aes=y -- evil_document.pdf evil_doc_enc.pdf

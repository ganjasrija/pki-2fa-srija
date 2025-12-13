#!/bin/bash
# Read commit data from stdin and pass to openssl
openssl pkeyutl -sign -inkey student_private.pem -passin env:KEY_PASSPHRASE -pkeyopt digest:sha256 -pkeyopt rsa_padding_mode:pss -pkeyopt rsa_pss_saltlen:max -in /dev/stdin

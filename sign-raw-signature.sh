#!/bin/bash
# Script to generate a raw RSA-PSS signature for Git

# Read the commit data (hash) from stdin.
read -r COMMIT_DATA

# Use OpenSSL to perform the RSA-PSS signing operation.
openssl pkeyutl -sign \
  -in <(echo -n "$COMMIT_DATA") \
  -inkey "$3" \
  -passin env:KEY_PASSPHRASE \
  -pkeyopt digest:sha256 \
  -pkeyopt rsa_padding_mode:pss \
  -pkeyopt rsa_pss_saltlen:max

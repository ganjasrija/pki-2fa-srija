#!/bin/bash
# Script to generate a raw RSA-PSS signature for Git (Universal Pipe Version)

# Read the entire commit data from standard input
COMMIT_DATA=$(cat)

# Use OpenSSL to perform the RSA-PSS signing operation.
# We pipe the data directly to openssl using 'echo -n "$COMMIT_DATA" | openssl ... -in -'
echo -n "$COMMIT_DATA" | openspenssl pkeyutl -sign \
  -inkey "$3" \
  -passin env:KEY_PASSPHRASE \
  -pkeyopt digest:sha256 \
  -pkeyopt rsa_padding_mode:pss \
  -pkeyopt rsa_pss_saltlen:max \
  -in -

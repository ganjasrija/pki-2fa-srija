#!/bin/bash
# Script to generate a raw RSA-PSS signature for Git (Most Compatible Version)

# Read the entire commit data from standard input into a single variable
COMMIT_DATA=$(cat)

# Use OpenSSL to perform the RSA-PSS signing operation.
# We pipe the data directly to openssl using '<<< "$COMMIT_DATA"'
openssl pkeyutl -sign \
  -inkey "$3" \
  -passin env:KEY_PASSPHRASE \
  -pkeyopt digest:sha256 \
  -pkeyopt rsa_padding_mode:pss \
  -pkeyopt rsa_pss_saltlen:max <<< "$COMMIT_DATA"

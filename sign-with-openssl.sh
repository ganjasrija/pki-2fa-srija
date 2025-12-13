#!/bin/bash
# Wrapper script to sign a commit hash using OpenSSL/student_private.pem

# Read the commit data from standard input
read -r COMMIT_HASH
# The private key file path is passed as the third argument
KEY_FILE="$3"

# Use openssl to generate an RSA-PSS signature on the ASCII bytes of the hash.
# The -passin env:KEY_PASSPHRASE handles both encrypted and unencrypted keys.
openssl pkeyutl -sign \
  -in <(echo -n "$COMMIT_HASH") \
  -inkey "$KEY_FILE" \
  -passin env:KEY_PASSPHRASE \
  -pkeyopt digest:sha256 \
  -pkeyopt rsa_padding_mode:pss \
  -pkeyopt rsa_pss_saltlen:max \
  | gpg --batch --passphrase-env KEY_PASSPHRASE --no-tty --detach-sign --no-version --default-key "$KEY_FILE" --output - 

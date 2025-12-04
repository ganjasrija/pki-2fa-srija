#!/bin/bash

# GitHub Repository URL
GITHUB_URL="https://github.com/yourusername/pki-2fa"

# Get the latest commit hash
COMMIT_HASH=$(git log -1 --format=%H)

# Read encrypted signature and remove line breaks
ENCRYPTED_SIGNATURE=$(tr -d '\n' < encrypted_signature.txt)

# Read student public key
STUDENT_PUBLIC_KEY=$(cat student_public.pem)

# Single line public key for API submission
STUDENT_PUBLIC_KEY_API=$(awk '{printf "%s\\n", $0}' student_public.pem)

# Read encrypted seed and remove line breaks
ENCRYPTED_SEED=$(tr -d '\n' < encrypted_seed.txt)

# Docker image URL (optional)
DOCKER_IMAGE_URL="docker.io/yourusername/pki-2fa:latest"

# Print submission info
echo -e "GitHub Repository URL:\n$GITHUB_URL\n"
echo -e "Commit Hash:\n$COMMIT_HASH\n"
echo -e "Encrypted Commit Signature (Base64, single line):\n$ENCRYPTED_SIGNATURE\n"
echo -e "Student Public Key (multi-line for form submission):\n$STUDENT_PUBLIC_KEY\n"
echo -e "Student Public Key (single line for API submission):\n$STUDENT_PUBLIC_KEY_API\n"
echo -e "Encrypted Seed (single line):\n$ENCRYPTED_SEED\n"
echo -e "Docker Image URL (optional):\n$DOCKER_IMAGE_URL\n"

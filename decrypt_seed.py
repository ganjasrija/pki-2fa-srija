import base64
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Path to files
PRIVATE_KEY_FILE = "student_private.pem"
ENCRYPTED_SEED_FILE = "encrypted_seed.txt"
SEED_FILE = "/data/seed.txt"

# Load your private key
with open(PRIVATE_KEY_FILE, "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
    )

# Load the encrypted seed from file
with open(ENCRYPTED_SEED_FILE, "r") as f:
    encrypted_seed_b64 = f.read().strip()

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    # 1. Base64 decode
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    # 2. Decrypt using RSA/OAEP with SHA-256
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. Decode to UTF-8
    decrypted_seed = decrypted_bytes.decode("utf-8")

    # 4. Validate: must be 64-character hex string
    if len(decrypted_seed) != 64 or any(c not in "0123456789abcdef" for c in decrypted_seed.lower()):
        raise ValueError("Invalid seed format")

    # 5. Return
    return decrypted_seed

# Decrypt seed
hex_seed = decrypt_seed(encrypted_seed_b64, private_key)

# Ensure /data folder exists (for Docker volume)
os.makedirs("/data", exist_ok=True)

# Save decrypted seed
with open(SEED_FILE, "w") as f:
    f.write(hex_seed)

print(f"✅ Seed decrypted and saved to {SEED_FILE}")

import base64
import os
import sys 
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Path to files
PRIVATE_KEY_FILE = "student_private.pem"
ENCRYPTED_SEED_FILE = "encrypted_seed.txt"
SEED_FILE = "/data/seed.txt" 

# --- SAFE KEY LOADING ---
try:
    with open(PRIVATE_KEY_FILE, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
        )
except FileNotFoundError:
    print(f"FATAL ERROR: Private key file not found at {PRIVATE_KEY_FILE}. Exiting.")
    sys.exit(1) 
except Exception as e:
    print(f"FATAL ERROR: Failed to load private key: {e}. Exiting.")
    sys.exit(1)

# --- SAFE ENCRYPTED SEED LOADING ---
try:
    with open(ENCRYPTED_SEED_FILE, "r") as f:
        encrypted_seed_b64 = f.read().strip()
except FileNotFoundError:
    print(f"FATAL ERROR: Encrypted seed file not found at {ENCRYPTED_SEED_FILE}. Exiting.")
    sys.exit(1)
except Exception as e:
    print(f"FATAL ERROR: Failed to read encrypted seed: {e}. Exiting.")
    sys.exit(1)


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

if __name__ == "__main__":
    try:
        hex_seed = decrypt_seed(encrypted_seed_b64, private_key)

        # Ensure /data folder exists (for Docker volume)
        os.makedirs(os.path.dirname(SEED_FILE), exist_ok=True)

        # Save decrypted seed
        with open(SEED_FILE, "w") as f:
            f.write(hex_seed)

        print(f"✅ Seed decrypted and saved to {SEED_FILE}")
    except Exception as e:
        print(f"FATAL DECRYPTION ERROR: {e}. Check key and encrypted seed integrity.")
        sys.exit(1)
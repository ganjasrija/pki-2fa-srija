from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from totp_utils import generate_totp_code, verify_totp_code
import time
from typing import Optional


app = FastAPI()
SEED_FILE = "/data/seed.txt" 
PRIVATE_KEY_FILE = "student_private.pem"

# Request models
class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class VerifyCodeRequest(BaseModel):
    code: str

# Helper function to load seed from file
def load_seed_from_file() -> Optional[str]:
    """Reads the seed from the persistent volume path."""
    if not os.path.exists(SEED_FILE):
        return None
    try:
        with open(SEED_FILE, "r") as f:
            return f.read().strip()
    except Exception:
        return None

# Endpoint 1: POST /decrypt-seed
@app.post("/decrypt-seed")
def decrypt_seed_endpoint(req: DecryptSeedRequest):
    try:
        # --- CRITICAL FIX 1: KEY LOADING SAFETY ---
        try:
            # Load private key
            with open(PRIVATE_KEY_FILE, "rb") as f:
                private_key = serialization.load_pem_private_key(f.read(), password=None)
        except FileNotFoundError:
            # Explicitly catch the error if the key is missing from the container
            raise HTTPException(status_code=500, detail=f"Private key file not found: {PRIVATE_KEY_FILE}")

        # Decode and decrypt seed
        encrypted_bytes = base64.b64decode(req.encrypted_seed)
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        hex_seed = decrypted_bytes.decode("utf-8")

        # Validate seed
        if len(hex_seed) != 64 or any(c not in "0123456789abcdef" for c in hex_seed.lower()):
            raise ValueError("Invalid seed format")

        # Save seed to /data/seed.txt (Correct path)
        os.makedirs(os.path.dirname(SEED_FILE), exist_ok=True)
        with open(SEED_FILE, "w") as f: 
            f.write(hex_seed)

        return {"status": "ok"}
    except HTTPException:
        # Re-raise explicit HTTP errors
        raise
    except Exception as e:
        # Catch decryption errors and return a clean 500 status
        raise HTTPException(status_code=500, detail=f"Decryption failed: {type(e).__name__}")


# Endpoint 2: GET /generate-2fa
@app.get("/generate-2fa")
def generate_2fa_endpoint():
    hex_seed = load_seed_from_file()
    if not hex_seed:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    code = generate_totp_code(hex_seed)

    # Calculate remaining seconds
    period = 30
    remaining = period - (int(time.time()) % period)

    return {"code": code, "valid_for": remaining}

# Endpoint 3: POST /verify-2fa
@app.post("/verify-2fa")
def verify_2fa_endpoint(req: VerifyCodeRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    hex_seed = load_seed_from_file()
    if not hex_seed:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    valid = verify_totp_code(hex_seed, req.code)
    return {"valid": valid}
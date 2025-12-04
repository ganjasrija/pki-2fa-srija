from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from totp_utils import generate_totp_code, verify_totp_code



app = FastAPI()
SEED_FILE = "/data/seed.txt"
PRIVATE_KEY_FILE = "student_private.pem"

# Request models
class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class VerifyCodeRequest(BaseModel):
    code: str

# Endpoint 1: POST /decrypt-seed
@app.post("/decrypt-seed")
def decrypt_seed_endpoint(req: DecryptSeedRequest):
    try:
        # Load private key
        with open(PRIVATE_KEY_FILE, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

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
        if len(hex_seed) != 64 or any(c not in "0123456789abcdef" for c in hex_seed):
            raise ValueError("Invalid seed format")

        # Save seed to /data/seed.txt
        os.makedirs(os.path.dirname(SEED_FILE), exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Decryption failed")

# Endpoint 2: GET /generate-2fa
@app.get("/generate-2fa")
def generate_2fa_endpoint():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)

    # Calculate remaining seconds
    import time
    period = 30
    remaining = period - (int(time.time()) % period)

    return {"code": code, "valid_for": remaining}

# Endpoint 3: POST /verify-2fa
@app.post("/verify-2fa")
def verify_2fa_endpoint(req: VerifyCodeRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    valid = verify_totp_code(hex_seed, req.code)
    return {"valid": valid}

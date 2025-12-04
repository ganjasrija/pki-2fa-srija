import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# 1. Replace with your latest commit hash
commit_hash = "2db507c53dd35627c107cf58f8f65926f4619753"

# 2. Load student private key
with open("student_private.pem", "rb") as f:
    student_private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,  # use your password if key is encrypted
        backend=default_backend()
    )

# 3. Sign commit hash using RSA-PSS-SHA256
def sign_message(message: str, private_key) -> bytes:
    return private_key.sign(
        message.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

signature = sign_message(commit_hash, student_private_key)

# 4. Load instructor public key
with open("instructor_public.pem", "rb") as f:
    instructor_public_key = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )

# 5. Encrypt signature using RSA-OAEP-SHA256
def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

encrypted_signature = encrypt_with_public_key(signature, instructor_public_key)

# 6. Base64 encode encrypted signature
proof = base64.b64encode(encrypted_signature).decode("utf-8")

# Output
print("Commit Hash:", commit_hash)
print("Encrypted Signature (Base64):", proof)

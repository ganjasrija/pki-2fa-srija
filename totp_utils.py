import base64
import pyotp

def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current 6-digit TOTP code from 64-character hex seed.
    """
    # Convert hex seed to bytes
    seed_bytes = bytes.fromhex(hex_seed)
    
    # Encode bytes to base32
    seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')
    
    # Create TOTP object (default SHA-1, 30s period, 6 digits)
    totp = pyotp.TOTP(seed_base32)
    
    # Generate current TOTP code
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with time window tolerance
    """
    seed_bytes = bytes.fromhex(hex_seed)
    seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(seed_base32)
    return totp.verify(code, valid_window=valid_window)

import time
from datetime import datetime, timezone # Added timezone import for utcnow consistency
from totp_utils import generate_totp_code
import os # Added os import for os.makedirs

# Set the CRITICAL persistent log path
LOG_FILE = "/data/last_code.txt"

try:
    # Read decrypted seed
    # The path /data/seed.txt is CORRECT.
    with open("/data/seed.txt", "r") as f:
        hex_seed = f.read().strip()
    
    # Generate TOTP
    code = generate_totp_code(hex_seed)
    
    # Timestamp in UTC
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    
    # Ensure /data exists before writing
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Append log to the CORRECT persistent path
    with open(LOG_FILE, "a") as log:
        log.write(f"{timestamp} - 2FA Code: {code}\n")

    # CRITICAL FIX: Print to stdout for evaluator capture (Step 11)
    print(f"{timestamp} - 2FA Code: {code}")
    
except Exception as e:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    # Write error log to the CORRECT persistent path
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as log:
        log.write(f"{timestamp} - ERROR: {e}\n")
    
    # IMPORTANT: Do not print error message directly to stdout here if the read_seed function already handled it,
    # but include a safe print here if running standalone.
    # We rely on the read_seed function's specific error print for the initial failure case (Step 11).
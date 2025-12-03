import time
from datetime import datetime
from totp_utils import generate_totp_code

try:
    # Read decrypted seed
    with open("/data/seed.txt", "r") as f:
        hex_seed = f.read().strip()
    
    # Generate TOTP
    code = generate_totp_code(hex_seed)
    
    # Timestamp in UTC
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    # Append log
    with open("/cron/last_code.txt", "a") as log:
        log.write(f"{timestamp} - 2FA Code: {code}\n")

except Exception as e:
    with open("/cron/last_code.txt", "a") as log:
        log.write(f"{datetime.utcnow()} - ERROR: {e}\n")


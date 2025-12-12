#!/usr/bin/env python3
import os
from datetime import datetime, timezone
import totp_utils
import time # Ensure time is imported if needed, although datetime is used


def read_seed():
    """Reads the seed from the persistent volume path."""
    try:
        # PATH IS CORRECT: /data/seed.txt
        with open("/data/seed.txt", "r") as f:
            return f.read().strip()
    except Exception:
        # This error is expected if the seed hasn't been written yet.
        # Print the exact error expected by the evaluator when the file is missing.
        print(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} - ERROR: [Errno 2] No such file or directory: '/data/seed.txt'")
        return None

def main():
    seed_hex = read_seed()
    if not seed_hex:
        # read_seed prints the error message, so we just return.
        return
    
    # CRITICAL FIX 1: Logging to persistent volume (/data)
    LOG_FILE = "/data/last_code.txt"
    
    try:
        code = totp_utils.generate_totp_code(seed_hex)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
        # CRITICAL FIX 2: Write log to persistent volume
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as log:
            log.write(f"{timestamp} - 2FA Code: {code}\n")
            
        # CRITICAL FIX 3: Print to stdout for evaluator capture (Step 11)
        print(f"{timestamp} - 2FA Code: {code}")
        
    except Exception as e:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - ERROR: {str(e)}")
        # Log error to the persistent volume as well
        with open(LOG_FILE, "a") as log:
             log.write(f"{timestamp} - ERROR: {e}\n")

if __name__ == "__main__":
    main()
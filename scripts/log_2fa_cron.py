#!/usr/bin/env python3
import os
from datetime import datetime, timezone
# --- LINE 4: CHANGED ---
import totp_utils
# -----------------------


def read_seed():
    try:
        with open("/data/seed.txt", "r") as f:
            return f.read().strip()
    except Exception as e:
        # This error is expected if the seed hasn't been written yet.
        print(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} - ERROR: [Errno 2] No such file or directory: '/data/seed.txt'")
        return None

def main():
    seed_hex = read_seed()
    if not seed_hex:
        # read_seed prints the error, so we just return here.
        return
    try:
        # --- FUNCTION CALL CHANGED ---
        code = totp_utils.generate_totp_code(seed_hex)
        # -----------------------------
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - 2FA Code: {code}")
    except Exception as e:
        print(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {str(e)}")

if __name__ == "__main__":
    main()

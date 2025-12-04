#!/usr/bin/env python3
import os
from datetime import datetime, timezone
from totp_utils import generate_totp_code




def read_seed():
    try:
        with open("/data/seed.txt", "r") as f:
            return f.read().strip()
    except Exception as e:
        return None

def main():
    seed_hex = read_seed()
    if not seed_hex:
        print(f"{datetime.now(timezone.utc)} - ERROR: Missing seed.txt")
        return

    try:
        code = generate_totp_code(seed_hex)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - 2FA Code: {code}")
    except Exception as e:
        print(f"{datetime.now(timezone.utc)} - ERROR: {str(e)}")

if __name__ == "__main__":
    main()


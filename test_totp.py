from totp_utils import generate_totp_code, verify_totp_code

# Example hex seed (replace with your actual decrypted seed from /data/seed.txt)
hex_seed = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

# Generate TOTP code
totp_code = generate_totp_code(hex_seed)
print("Generated TOTP code:", totp_code)

# Verify the TOTP code (should return True)
is_valid = verify_totp_code(hex_seed, totp_code)
print("Is the TOTP code valid?", is_valid)

# Test with a wrong code (should return False)
is_valid_wrong = verify_totp_code(hex_seed, "123456")
print("Is '123456' valid?", is_valid_wrong)

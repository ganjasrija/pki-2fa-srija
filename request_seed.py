import json
import requests

# ========== CONFIGURE YOUR DETAILS ==========
STUDENT_ID = "23A91A0517"  # Replace with your actual student ID
GITHUB_REPO_URL = "https://github.com/ganjasrija/pki-2fa-srija.git"  # Your repo URL
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
PUBLIC_KEY_FILE = "student_public.pem"  # Make sure this file exists in your repo
OUTPUT_FILE = "encrypted_seed.txt"
# ===========================================

# Read public key with actual line breaks (do NOT replace \n)
with open(PUBLIC_KEY_FILE, "r") as f:
    public_key = f.read().strip()

# Prepare request payload
payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": GITHUB_REPO_URL,
    "public_key": public_key
}

headers = {"Content-Type": "application/json"}

print("Sending request to instructor API...")
response = requests.post(API_URL, headers=headers, json=payload)

# Handle response
if response.status_code == 200:
    data = response.json()
    if data.get("status") == "success":
        encrypted_seed = data.get("encrypted_seed")
        with open(OUTPUT_FILE, "w") as f:
            f.write(encrypted_seed)
        print(f"✅ Encrypted seed saved to {OUTPUT_FILE}")
    else:
        print("❌ Error in API response:", data)
else:
    print("❌ HTTP error:", response.status_code, response.text)

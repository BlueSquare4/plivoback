import json
import base64

print("Paste your entire Firebase JSON below. Finish with an empty line:")

# Step 1: Read multi-line JSON from user
lines = []
while True:
    line = input()
    if line.strip() == "":
        break
    lines.append(line)

raw_json = "\n".join(lines)

# Step 2: Validate it's valid JSON (optional, but safe)
try:
    json.loads(raw_json)  # will raise if invalid
except Exception as e:
    print("❌ Invalid JSON. Error:", e)
    exit(1)

# Step 3: Encode to base64
encoded = base64.b64encode(raw_json.encode("utf-8")).decode("utf-8")

# Step 4: Print the .env-ready output
print("\n✅ Paste this in your .env file:\n")
print(f"FIREBASE_CREDENTIAL_BASE64={encoded}")

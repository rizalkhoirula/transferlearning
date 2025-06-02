import os
import json
import requests
from dotenv import load_dotenv

print("Step 1: Loading environment variables...")
load_dotenv()

BAICHUAN_API = os.getenv("BAICHUAN_API")
print(f"Step 2: BAICHUAN_API = {BAICHUAN_API}")

if not BAICHUAN_API:
    print("❌ Error: BAICHUAN_API not found in environment variables.")
    exit()

headers = {
    "Authorization": f"Bearer {BAICHUAN_API}",
    "Content-Type": "application/json"
}

prompt = "Sebutkan nama buah-buahan tropis dalam format JSON: {'buah_1': '...', 'buah_2': '...'}"

payload = {
    "model": "Baichuan2-Turbo",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
}

api_url = "https://api.baichuan-ai.com/v1/chat/completions"

try:
    print(f"Step 3: Sending prompt to Baichuan model at {api_url} ...")
    response = requests.post(api_url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    response_json = response.json()
    print("✅ Response received:")
    print(json.dumps(response_json, indent=2, ensure_ascii=False))

    # Mengambil dan mencetak isi respons
    if "choices" in response_json and len(response_json["choices"]) > 0:
        content = response_json["choices"][0]["message"]["content"]
        print("\nGenerated text:")
        print(content)
    else:
        print("\n❌ Response format tidak seperti yang diharapkan.")

except requests.exceptions.HTTPError as http_err:
    print(f"❌ HTTP error occurred: {http_err}")
except Exception as e:
    print(f"❌ An error occurred: {e}")

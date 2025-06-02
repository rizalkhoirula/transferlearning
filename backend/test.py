import requests

url = "https://api.baichuan-ai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-b231b0c9f682c2e8738453fe144a385c"  # Ganti dengan API Key kamu
}

data = {
    "model": "Baichuan2-Turbo",
    "messages": [
        {"role": "user", "content": "请用中文解释量子物理是什么？"}
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())

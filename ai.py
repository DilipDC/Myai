
import requests, os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_ai(prompt):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model":"deepseek/deepseek-chat",
        "messages":[
            {"role":"user","content":prompt}
        ]
    }

    try:
        r = requests.post(url, headers=headers, json=data, timeout=30)
        res = r.json()
        return res["choices"][0]["message"]["content"]
    except Exception as e:
        return "AI connection error: " + str(e)

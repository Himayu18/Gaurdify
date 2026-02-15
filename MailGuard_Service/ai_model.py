import os
import json
import requests
from dotenv import load_dotenv
load_dotenv() 

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def classify_email(subject: str, body: str, model: str = "nvidia/nemotron-3-nano-30b-a3b:free") -> dict:
    system = (
        "You are a spam classifier for emails. "
        "Return ONLY valid JSON with keys: label, score, reasons, signals. "
        "label must be one of: spam, not_spam, suspicious. "
        "score is 0.0 to 1.0 where 1.0 is definitely spam. "
        "Keep reasons short and non-sensitive."
    )
    user = {
        "subject": subject[:500],   
        "body": body[:4000]
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user)}
        ],
        "temperature": 0.0
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "MailGuard"
    }
    r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
    r.raise_for_status()

    content = r.json()["choices"][0]["message"]["content"]

    return json.loads(content)

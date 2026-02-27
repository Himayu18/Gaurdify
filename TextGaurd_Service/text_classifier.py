import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
ALLOWED_CATEGORIES = {"sincere", "sarcastic", "abusive", "neutral"}

def evaluate_message(message: str, model: str = "nvidia/nemotron-3-nano-30b-a3b:free") -> dict:
    if not OPENROUTER_API_KEY:
        return {"error": "AI service configuration error: Missing API key."}

    if not message or not isinstance(message, str):
        return {"error": "Invalid input: message must be a non-empty string."}

    system = (
        "You are a strict message evaluation system.\n"
        "Return ONLY valid JSON with keys:\n"
        "is_normal, sincerity_score, confidence, category, signals.\n\n"
        "Rules:\n"
        "- category MUST be exactly one of: sincere, sarcastic, abusive, neutral.\n"
        "- sincerity_score must be between 0.0 and 1.0.\n"
        "- confidence must be between 0.0 and 1.0.\n"
        "- signals must be a short list of textual cues.\n"
        "- If unsure about category, use 'neutral'.\n"
        "- Do NOT output anything except JSON.\n"
    )

    user = {"message": message[:2000]}

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
        "X-Title": "MessageGuard"
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            return {
                "error": f"AI service returned HTTP {response.status_code}."
            }

        data = response.json()

        if "choices" not in data or not data["choices"]:
            return {
                "error": "AI service returned an unexpected response structure."
            }

        content = data["choices"][0]["message"]["content"]

    except requests.Timeout:
        return {"error": "AI service timeout. Please try again."}

    except requests.RequestException as e:
        return {
            "error": "Failed to connect to AI service.",
            "details": str(e)
        }

    except Exception as e:
        return {"error": "Unexpected error while contacting AI service.","details": str(e)}
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        return {"error": "AI returned invalid JSON format."}

    category = str(result.get("category", "")).lower().strip()

    if category == "normal":
        category = "neutral"

    if category not in ALLOWED_CATEGORIES:
        category = "neutral"

    def clamp(value):
        try:
            value = float(value)
            return max(0.0, min(1.0, value))
        except:
            return 0.0

    sincerity_score = clamp(result.get("sincerity_score"))
    confidence = clamp(result.get("confidence"))

    is_normal = category in {"sincere", "neutral"}

    return {
        "is_normal": is_normal,
        "sincerity_score": sincerity_score,
        "confidence": confidence,
        "category": category,
        "signals": result.get("signals", [])
    }
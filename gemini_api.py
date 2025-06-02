# gemini_api.py
import requests

API_KEY = "AIzaSyCTarY2dZLjkaaJOLlBKDG9IxwDeExvOzY"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

HEADERS = {
    "Content-Type": "application/json"
}

def summarize_text(text, length='short'):
    prompt = f"Summarize the following text in a {length} format:\n\n{text}"
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(ENDPOINT, headers=HEADERS, json=data)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {e}"

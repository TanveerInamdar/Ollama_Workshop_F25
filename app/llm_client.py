"""Ollama API client"""
import requests

API_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"


def generate_response(messages, prompt):
    """Send prompt to Ollama and get response"""
    # Build conversation history (exclude last user message, it's in prompt)
    history = messages[:-1] if messages else []
    full_prompt = "".join(f"{m['role'].title()}: {m['content']}\n" for m in history)
    full_prompt += f"User: {prompt}\nAssistant:"
    
    try:
        resp = requests.post(
            API_URL,
            json={"model": MODEL, "prompt": full_prompt, "stream": False},
            timeout=120
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip() or "❌ Empty response"
    
    except requests.exceptions.ConnectionError:
        return "❌ Ollama not running. Start with: ollama serve"
    except requests.exceptions.Timeout:
        return "❌ Timeout"
    except Exception as e:
        return f"❌ Error: {e}"

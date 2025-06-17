import os
import time
import requests
from seversdk.load_metrics import Metrics

# Если Ollama слушает нестандартный адрес/порт, укажите здесь:
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

MODEL = "deepseek-r1:32b"

def pipe(prompt: str, metrics) -> str:
    url = f"{metrics.yamlConfing['ollama_url']}/api/chat"
    payload = {
        "model": metrics.yamlConfing["model_name"],
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    # В зависимости от версии API ключ может называться 'message' или 'choices'
    if "message" in data:
        return data["message"]["content"]
    elif "choices" in data and data["choices"]:
        return data["choices"][0]["message"]["content"]
    else:
        raise RuntimeError(f"Unexpected Ollama response format: {data}")
import requests
import json

# Sostituisci <OPENROUTER_API_KEY> con la tua chiave API reale
OPENROUTER_API_KEY = "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"

response = requests.get(
    url="https://openrouter.ai/api/v1/auth/key",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }
)

print(json.dumps(response.json(), indent=2))
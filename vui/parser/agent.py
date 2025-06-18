import requests
import json
import re
#TODO Aggiungere funzionalità offline senza LLM in caso di erorre di connessione internet
class Agent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "mistralai/devstral-small:free"
        
        # Prompt fisso nel system message (istruzioni generali)
        self.system_prompt = (
            "Estrai i seguenti dati strutturati dalla frase che segue. Rispondi *solo* con un oggetto JSON valido e non aggiungere testo fuori dal JSON.\n\n"
            "Dati da estrarre:\n"
            '- "intent": se il testo parla di creazione del Digital Twin, usa "crea"; se parla di simulazione, usa "simula"\n'
            '- "paziente": il nome completo del paziente\n'
            '- "data": la data menzionata nel testo\n'
            '- "terapia": SOLO se si parla di simulazione\n\n'
            "Formato di risposta:\n"
            "{\n"
            '  "intent": "...",\n'
            '  "paziente": "...",\n'
            '  "data": "...",\n'
            '  "terapia": "..." // solo se c\'è\n'
            "}"
        )

    def extract_json(self, text):
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                return None
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None

    def ask(self, user_text):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Costruiamo i messaggi per la chat
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f'Testo:\n"{user_text}"'}
        ]
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.0  # temperatura bassa per risposte più precise
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        result_text = response.json()["choices"][0]["message"]["content"]
        
        parsed = self.extract_json(result_text)
        if parsed is None:
            return {
                "error": "Risposta non è un JSON valido",
                "raw_response": result_text
            }
        return parsed

import json
import re
from openai import OpenAI


class Agent:
    def __init__(self, api_key, prompt=None, site_url=None, site_name=None):
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        # Headers extra (facoltativi ma consigliati per ranking OpenRouter)
        self.extra_headers = {}
        if site_url:
            self.extra_headers["HTTP-Referer"] = site_url
        if site_name:
            self.extra_headers["X-Title"] = site_name

        self.model = "deepseek/deepseek-chat-v3-0324:free"

        self.system_prompt = prompt
        print(f"Agent initialized with model: {self.model}")
        print(f"System prompt: {self.system_prompt}")
        print(f"Extra headers: {self.extra_headers}")
    def extract_json(self, text):
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                return None
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None

    def ask(self, user_text):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f'Testo:\n"{user_text}"'},
                ],
                temperature=0.0,
                extra_headers=self.extra_headers,
            )

            result_text = response.choices[0].message.content
            parsed = self.extract_json(result_text)
            if parsed is None:
                return {
                    "error": "Risposta non è un JSON valido",
                    "raw_response": result_text,
                }
            return parsed

        except Exception as e:
            return {"error": f"Errore durante la chiamata API: {e}"}


class MedicalAgent:
    def __init__(self, api_key,prompt=None):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = "mistralai/devstral-small:free"
        self.system_prompt = prompt

    def ask(self, simulation_objects):
        prompt = self._build_prompt(simulation_objects)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Errore: {e}"

    def _build_prompt(self, objects):
        # Aggiunge i dati come JSON formattati
        return f"Ecco i dati delle simulazioni:\n{json.dumps(objects, indent=2)}"
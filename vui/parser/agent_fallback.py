from nano_llm_wrapper import NanoLLMFallback  # Assicurati che il path sia corretto
import json
import re
from openai import OpenAI

class Agent:
    def __init__(self, api_key, prompt=None, site_url=None, site_name=None, llm_fallback=None):
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        self.extra_headers = {}
        if site_url:
            self.extra_headers["HTTP-Referer"] = site_url
        if site_name:
            self.extra_headers["X-Title"] = site_name

        self.model = "deepseek/deepseek-chat-v3-0324:free"
        self.system_prompt = prompt

        self.llm_fallback = llm_fallback or NanoLLMFallback()

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
            return self._fallback(user_text, error=str(e))

    def _fallback(self, user_text, error=None):
        try:
            response = self.llm_fallback.ask(user_text)
            parsed = self.extract_json(response)
            if parsed is None:
                return {
                    "error": f"Fallback LLM non ha restituito un JSON valido.",
                    "raw_response": response
                }
            return {
                "error": f"Errore nella chiamata API, fallback LLM attivo. {error}",
                "result": parsed,
                "note": "Risposta generata con modello nano-vllm"
            }
        except Exception as llm_error:
            return {
                "error": f"Errore nel fallback nano-LLM: {llm_error}",
                "note": "Verifica che il modello sia correttamente avviato"
            }

class MedicalAgent:
    def __init__(self, api_key, prompt=None, llm_fallback=None):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = "mistralai/devstral-small:free"
        self.system_prompt = prompt

        self.llm_fallback = llm_fallback or NanoLLMFallback()

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
            return self._fallback(simulation_objects, error=str(e))

    def _build_prompt(self, objects):
        return f"Ecco i dati delle simulazioni:\n{json.dumps(objects, indent=2)}"

    def _fallback(self, simulation_objects, error=None):
        try:
            # Trasformo gli oggetti in stringa da passare a nano-llm
            prompt = self._build_prompt(simulation_objects)
            response = self.llm_fallback.ask(prompt)
            return response.strip()

        except Exception as llm_error:
            return f"Errore nel fallback nano-LLM: {llm_error} | Errore originale: {error}"
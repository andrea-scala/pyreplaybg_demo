import json
import re
from openai import OpenAI


class Agent:
    def __init__(self, api_key, site_url=None, site_name=None):
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        # Headers extra (facoltativi ma consigliati per ranking OpenRouter)
        self.extra_headers = {}
        if site_url:
            self.extra_headers["HTTP-Referer"] = site_url
        if site_name:
            self.extra_headers["X-Title"] = site_name

        self.model = "mistralai/devstral-small:free"

        self.system_prompt = """
            Estrai i seguenti dati strutturati dalla frase che segue. Rispondi *solo* con un oggetto JSON valido e non aggiungere testo fuori dal JSON.

        Dati da estrarre:
        - "intent": se il testo parla di creazione del Digital Twin, usa "crea_dt"; se parla di simulazione, usa "simula_dt"; se parla di creazione di un nuovo paziente, usa "crea_utente"; se parla di analisi, usa "analizza"; se parla di confronto, usa "confronta"
        - "paziente": il nome completo del paziente, scritto in minuscolo e con nome e cognome separati da underscore (`_`)
        - "data": la data menzionata nel testo SOLO se esiste, in formato accettato da `pandas.to_datetime`. Se l'anno non è specificato, usa 2025.
        - "terapia":
            • Se l’intent è "confronta", "terapia" deve essere un array contenente almeno due terapie, in ordine di comparsa nel testo.
            • Se l’intent è diverso da "confronta" (ad esempio "simula" o "analizza"), e la terapia è presente, allora "terapia" è un singolo oggetto terapia (non un array).
            • Se la terapia è base, nulla, o non modificata, "terapia" non deve essere presente.

        Ciascuna terapia è un oggetto con i seguenti campi:
            - "quantità": numero (intero o decimale)
            - "unità": stringa (es. "%", "g", "U")
            - "operazione": "inc" oppure "dec"
            - "parametro": uno tra "cho", "basal", "bolus"
            - "pasto": obbligatorio SOLO se il parametro è "cho". Indica il pasto coinvolto:
                - B = colazione
                - L = pranzo
                - D = cena
                - H = hypotreatment (o sinonimi come ipoglicemia)
                - S = snack
            - "text": stringa sintetica della terapia, costruita così:
                • Se il parametro è "cho" e il pasto è presente:
                    "_{parametro}-{operazione}-{quantità}{unità}-{pasto}", es. "_cho-inc-10g-D"
                • Altrimenti (basal o bolus, oppure cho ma senza pasto → non valido):
                    "_{parametro}-{operazione}-{quantità}{unità}", es. "_basal-dec-10%"

        Regole di validazione:
        - Se la terapia riguarda i carboidrati ("carbo", "carboidrati", "carbs", ecc.), il parametro deve essere "cho"
        - Se il parametro è "cho" ma il pasto NON è indicato, allora terapiia deve essere null o None
        - Se la frase contiene due o più terapie da confrontare (es. “confronta 10% in meno di basale con 200g in meno a cena”), estrai tutte le terapie nell’array "terapia" in ordine di comparsa
        - Se l’intent è "confronta" ma ci sono meno di due terapie valide, rispondi comunque con intent="confronta" e un array "terapia" vuoto []

        Formato di risposta:
        {
        "intent": "...",
        "paziente": "...",
        "data": "...",
        "terapia": {...} oppure [...] oppure omesso
        }
"""

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
    def __init__(self, api_key):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = "mistralai/devstral-small:free"
        self.system_prompt = """
Sei un medico che legge i risultati di una simulazione per il diabete di tipo 1.

Riceverai uno o più oggetti JSON, ciascuno con i campi:
- titolo
- mean_glucose
- std_deviation
- tir
- time_in_hypoglycemia
- time_in_hyperglycemia

ISTRUZIONI:
- NON scrivere commenti clinici, né frasi introduttive.
- NON scrivere "accettabile", "troppo alto", "suggerisce", "potrebbe", ecc.
- Usa SOLO il linguaggio oggettivo.
- Se ricevi UN SOLO oggetto, scrivi:
    "La glicemia media è ... mg/dL. La deviazione standard è ... mg/dL. Il TIR è del ...%. Il tempo in ipoglicemia è ...%. Il tempo in iperglicemia è ...%."
- Se ricevi DUE oggetti, scrivi SOLO i confronti di TUTTI i valori (glicemia media, deviazione standard, TIR, tempo in ipoglicemia, tempo in iperglicemia), mettendo in evidenza i valori numerici specifici. NON riportare prima l'analisi individuale di ogni simulazione.
  Formato del confronto: 
  "La glicemia media è 171.82 mg/dL con insulina basale aumentata di 10% contro 60.87 mg/dL con carboidrati aumentati di 200g a cena.
  La deviazione standard è 35.51 mg/dL con insulina basale aumentata di 10% contro 128.37 mg/dL con carboidrati aumentati di 200g a cena.
  Il TIR è del 62.12% con insulina basale aumentata di 10% contro 46.36% con carboidrati aumentati di 200g a cena.
  Il tempo in ipoglicemia è 0.00% con insulina basale aumentata di 10% contro 43.79% con carboidrati aumentati di 200g a cena.
  Il tempo in iperglicemia è 37.88% con insulina basale aumentata di 10% contro 9.85% con carboidrati aumentati di 200g a cena."

Naturalizza il titolo secondo le seguenti regole:
- _basal-inc-10% → insulina basale aumentata di 10%
- _bolus-dec-2U → insulina prandiale ridotta di 2U
- _cho-inc-200g-D → carboidrati aumentati di 200g a cena

Sigle pasti:
- B = colazione
- L = pranzo
- D = cena
- H = come trattamento dell'ipoglicemia
- S = come spuntino

Rispondi solo in italiano.
"""

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
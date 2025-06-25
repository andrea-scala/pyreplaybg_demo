from bottle import *
import io
import tempfile
from vui.s2t.audio_transcriber import AudioTranscriber
from vui.parser.agent import Agent, MedicalAgent
import vui.parser.parser as parser
import json
import os
from dotenv import load_dotenv

# @route("/get_prompt", method=["POST"])
# def get_prompt():
#     audio_file = request.files.get('audio')  # <-- questa è la chiave usata in formData.append()
#     if audio_file:
#         audio_file_bytes = io.BytesIO(audio_file.file.read())
#         with tempfile.NamedTemporaryFile(suffix=".m4a") as temp_file:
#             temp_file.write(audio_file_bytes.getbuffer())
#             temp_file.flush()
#             transcribed_text = transcriber.transcribe_text_only(temp_file.name)
#             print(f"Transcribed text: {transcribed_text}")
#             result = agent.ask(transcribed_text)
#             print(f"Output LLM: {result}")
#             parser_results = parser.parse_output(result)
#             print(f"Parser Results: {parser_results}")
#             medical_agent_results = medicalAgent.ask(parser_results)
#             print(medical_agent_results)
#             return medical_agent_results

paziente = "Mario Rossi"
data = "6 maggio 25"
prompts = [
        f"Crea il twin di {paziente} per la data {data}",
        f"Simula per {paziente} per il giorno {data} la terapia base",
        f"Simula per {paziente} per il giorno {data} la terapia con 200gr di carboidrati",
        f"Analizza per {paziente} per il giorno {data} la terapia con 200gr di carboidrati",
        f"Simula per {paziente} per il giorno {data} la terapia con 200gr di carboidrati in più a cena",
        f"Analizza per {paziente} per il giorno {data} la terapia con 200gr di carboidrati in più a cena",
        f"Confronta per {paziente} per il giorno {data} la terapia con 200gr di carboidrati in più a cena con la terapia base",
        f"Vorrei sapere cosa succede a {paziente} per il giorno {data} se mangia 200gr di carboidrati in meno a cena",
        f"Analizza cosa succede a {paziente} per il giorno {data} se mangia 200gr di carboidrati in meno a cena",
]


@route("/get_prompt", method=["GET"])
def get_prompt_get():
    idx = int(request.query.get('idx', 0))
    if idx < 0 or idx >= len(prompts):
        return {"error": "Indice prompt non valido"}
    transcribed_text = prompts[idx]
    print(f"Transcribed text (GET): {transcribed_text}")
    result = agent.ask(transcribed_text)
    print(f"Output LLM: {result}")
    parser_results = parser.parse_output(result)
    print(f"Parser Results: {parser_results}")
    medical_agent_results = medicalAgent.ask(parser_results)
    print(medical_agent_results)
    return medical_agent_results

@route("/")
def index():
    return template("index.tpl")

@route("/get_prompt", method=["POST"])
def get_prompt():
    audio_file = request.files.get('audio')  # <-- questa è la chiave usata in formData.append()
    if audio_file:
        audio_file_bytes = io.BytesIO(audio_file.file.read())
        with tempfile.NamedTemporaryFile(suffix=".m4a") as temp_file:
            temp_file.write(audio_file_bytes.getbuffer())
            temp_file.flush()
            transcribed_text = transcriber.transcribe_text_only(temp_file.name)
            print(f"Transcribed text: {transcribed_text}")
            result = {"stato":1,"messaggio": "Trascrizione effettuata.","risultato":transcribed_text}
            print("type of result:", type(result))
            return {"stato":1,"messaggio": "Conversione in testo effettuata.","risultato":transcribed_text}
    return {
        "stato":0,"messaggio": "Errore, riprova ad inviare il prompt.","risultato": False
    }
    
@route("/to_json", method=["POST"])
def to_json():
    prompt = request.params.get('prompt')    
    agent_response = agent.ask(prompt)
    print(type(agent_response))
    print(agent_response)
    return {"stato":1,"messaggio": "Risposta dell'agent ottenuta.","risultato":agent_response}

@route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="static")


try:
    with open(os.path.join("vui","parser","config.json"), encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    with open(os.path.join("parser","config.json"), encoding="utf-8") as f:
        config = json.load(f)
load_dotenv()  # carica variabili da .env
api_key = os.getenv("OPENAI_API_KEY")
# print(api_key)
# print(config)
transcriber = AudioTranscriber()
agent = Agent(api_key=api_key,prompt=config["prompt1"])
medicalAgent = MedicalAgent(api_key=api_key,prompt=config["prompt2"])
run(host="localhost", port=8080, debug=True, reloader=True)

from s2t.audio_transcriber import AudioTranscriber
from parser.agent import Agent, MedicalAgent
import parser.parser as parser
import json
import os
from dotenv import load_dotenv

def main():
    try:
        with open(os.path.join("vui","parser","config.json"), encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        with open(os.path.join("parser","config.json"), encoding="utf-8") as f:
            config = json.load(f)

    load_dotenv()  # carica variabili da .env

    api_key = os.getenv("OPENAI_API_KEY")
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

    transcriber = AudioTranscriber()
    agent = Agent(api_key=api_key,prompt=config["prompt1"])
    medicalAgent = MedicalAgent(api_key=api_key,prompt=config["prompt2"])
    for prompt in prompts:
        # print(f"\nTranscribing audio: {audio_path} ...")
        # Usa la trascrizione reale quando pronta
        # transcribed_text = transcriber.transcribe_text_only(audio_path)

        # Per ora usiamo testo simulato
        transcribed_text = prompt
        print("Transcribed text:")
        print(transcribed_text)

        result = agent.ask(transcribed_text)
        print("Output LLM:")
        print(result)

        parser_results = parser.parse_output(result)
        print("Parser Results:")
        print(parser_results)
        medical_agent_results = medicalAgent.ask(parser_results)
        print("Medical Agent Output:")
        print(medical_agent_results)



if __name__ == "__main__":
    main()

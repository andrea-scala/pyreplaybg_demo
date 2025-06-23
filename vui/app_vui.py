from s2t.audio_transcriber import AudioTranscriber
from parser.agent import Agent, MedicalAgent
import parser.parser as parser
import json
import os
from dotenv import load_dotenv

def main():
    with open("parser/config.json", encoding="utf-8") as f:
        config = json.load(f)

    load_dotenv()  # carica variabili da .env

    api_key = os.getenv("OPENAI_API_KEY")
    
    prompts = [
         "Simula per Mario Rossi per il 5 maggio 2025 la terapia con 200gr di carbo in più a cena",
         "Simula per Mario Rossi per il 5 maggio 2025 la terapia con 10% di basale in più",
     "analizza per Mario Rossi per il 5 maggio 2025 la terapia con 200gr di carbo in più a cena",
     "analizza per Mario Rossi per il 5 maggio 2025 la terapia con 10% di basale in più",
     "confronta per Mario Rossi per il 5 maggio 2025 la terapia con 200gr di carbo in più a cena con la terapia con 10% di basale in più",
    "analizza per Mario Rossi per il 5 maggio 2025 la terapia con 200gr di carbo in più",
    "simula per Mario Rossi per il 5 maggio 2025 la terapia con 10% di carbo in più",
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

from s2t.audio_transcriber import AudioTranscriber
from parser.agent import Agent
import json
with open("parser/config.json") as f:
    config = json.load(f)

API_KEY = config.get("api_key", "")
AUDIO_PATH = "crea.m4a"

if __name__ == "__main__":
    transcriber = AudioTranscriber()

    #1 trascrizione
    print("Transcribing audio...")
    transcribed_text = transcriber.transcribe_text_only(AUDIO_PATH)
    print("Transcribed text:")
    print(transcribed_text)

    #2 Test LLM
    agent = Agent(API_KEY)
    result = agent.ask(transcribed_text)
    print("Output LLM:", result)
    #Da sostituire con Parsing con LLM
    
    #3 Parsing con LLM
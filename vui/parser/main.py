from agent import Agent
import json

with open("config.json") as f:
    config = json.load(f)
api_key = config.get("api_key", "")

agent = Agent(api_key)

testo = (
    "Crea un Digital Twin per il paziente Mario Rossi, per il giorno 15 marzo 2024. "
)
result = agent.ask(testo)
print("Output estratto:", result)

testo_simulazione = ( "Simula per Mario Rossi, per il giorno 15 marzo 2024, la terapia con 15gr di carboidrati in meno")
result_simulazione = agent.ask(testo_simulazione)
print("Output estratto simulazione:", result_simulazione)

testo_crea_utente = (
    "Crea un nuovo paziente, Mario Rossi, con peso 70kg e insulina basale 0.244"
)
result_crea_utente = agent.ask(testo_crea_utente)
print("Output estratto creazione utente:", result_crea_utente)
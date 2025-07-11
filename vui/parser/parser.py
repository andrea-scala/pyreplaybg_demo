import os
import csv
import sys

# Calcola il path assoluto della root del progetto (due livelli sopra questo file)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import utils

SAVE_FOLDER = os.path.abspath("..")


def crea_paziente(result_json):
    paziente = result_json.get("paziente")
    peso = result_json.get("peso")
    u2ss = result_json.get("u2ss")
    print(f"[CREA PAZIENTE] Nome: {paziente}, Peso: {peso}kg, U2SS: {u2ss}")
    #     # Crea cartella se non esiste
    #     base_dir = "../patient_data"
    #     os.makedirs(base_dir, exist_ok=True)
    #     # Normalizza il nome: minuscolo, spazi sostituiti con underscore
    #     nome_file = paziente.strip().lower().replace(" ", "_") + ".csv"
    #     csv_path = os.path.join(base_dir, nome_file)
    #     if os.path.exists(csv_path):
    #         print(f"[CSV ESISTE] Il file {csv_path} esiste già, non verrà sovrascritto.")
    #         return
    #     # Scrive il CSV con le colonne richieste
    #     with open(csv_path, mode="w", newline="") as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=["patient", "u2ss", "bw"])
    #         writer.writeheader()
    #         writer.writerow({
    #             "patient": 1,
    #             "u2ss": u2ss,
    #             "bw": peso
    #         })
    #     print(f"[CSV CREATO] File salvato in: {csv_path}")

def crea_dt(result_json):
    paziente = result_json.get("paziente")
    data = result_json.get("data")
    #Log
    print(f"[CREA DIGITAL TWIN] Paziente: {paziente}, Data: {data}")

    # Carica informazioni del paziente
    patient_info_path = f"../patient_data/{paziente}.csv"
    patient_info = utils.load_patient_info(patient_info_path)
    if patient_info.empty:
        #log
        print(f"[ERRORE] Paziente {paziente} non trovato ({patient_info_path}).")
        #il messaggio da dare al t2s
        #print(f"Il paziente {paziente} non esiste. Crea prima il paziente.")
        return

    # Carica dati giornalieri
    day_data_path = f"../patient_data/{paziente}_{data}.csv"
    day_data = utils.load_test_data(day_data_path)
    if day_data.empty:
        #Log
        print(f"[ERRORE] Dati per il giorno {data} non trovati ({day_data_path}).")
        # il messaggio da dare al t2s
        #print(f"I dati per il giorno {data} non esistono.")
        return

    # Percorso di salvataggio
    save_name = f"{paziente}_{data}"
    map_file_name = f"map_{save_name}.pkl"
    file_path = os.path.join(SAVE_FOLDER, "results", "map", map_file_name)

    if os.path.exists(file_path):
        # Log
        print(
            f"[ERRORE] Il twin per {paziente} per il giorno {data} esiste già: {file_path}"
        )
        # Il messaggio da dare al t2s
        # print(f"Il twin per {paziente} per il giorno {data} esiste già. Non verrà sovrascritto.")
        return

    #log
    print(f"[OK] Creazione del twin in corso...")
    # il messaggio da dare al t2s
    # print(f"Creazione del twin per {paziente} per il giorno {data} in corso")
    twin_results = utils.twin(patient_info, day_data, save_name, SAVE_FOLDER)
    if not twin_results:
        #Log
        print(
            f"[ERRORE] Creazione del twin fallita per {paziente} per il giorno {data}."
        )
        # il messaggio da dare al t2s
        # print(f"Creazione del twin per {paziente} per il giorno {data} fallita.")
        return
    #Log
    print(f"[OK] Twin creato e salvato in {file_path}")
    # il messaggio da dare al t2s
    # print(f"Twin del paziente {paziente} per il giorno {data} creato.")

def simula_dt(result_json):
    paziente = result_json.get("paziente")
    terapia = result_json.get("terapia")
    data = result_json.get("data")
    # Log
    print(f"[SIMULA DT] Paziente: {paziente}, Terapia: {terapia}, Data: {data}")
    

    # Carica informazioni del paziente
    patient_info_path = f"../patient_data/{paziente}.csv"
    patient_info = utils.load_patient_info(patient_info_path)
    if patient_info.empty:
        # Log
        print(f"[ERRORE] Paziente {paziente} non trovato ({patient_info_path}).")
        # il messaggio da dare al t2s
        # print(f"Il paziente {paziente} non esiste. Crea prima il paziente.")
        return

    # Carica dati giornalieri
    day_data_path = f"../patient_data/{paziente}_{data}.csv"
    day_data = utils.load_test_data(day_data_path)
    if day_data.empty:
        # Log
        print(f"[ERRORE] Dati per il giorno {data} non trovati ({day_data_path}).")
        # il messaggio da dare al t2s
        # print(f"I dati per il giorno {data} non esistono.")
        return
    
    #Esiste il dt del paziente?
    save_name = f"{paziente}_{data}"
    map_file_name = f"map_{save_name}.pkl"
    file_path = os.path.join(SAVE_FOLDER, "results", "map", map_file_name)

    if not os.path.exists(file_path):
        #Log
        print(
            f"[ERRORE] Il twin per {paziente} per il giorno {data} non esiste: {file_path}"
        )
        # Il messaggio da dare al t2s
        # print(f"Il twin per {paziente} per il giorno {data} non esiste. Crea prima il twin.")
        return
    #Log
    print(f"[OK] Twin trovato: {file_path}")
    # utils.show_data_head(data=day_data, n=50)
    #Se la terapia è false o null, non applicare alcuna terapia
    if not terapia or terapia == "base" or terapia == "nessuna":
        #Log
        print("[INFO] Terapia base o nessuna. Nessuna modifica applicata.")
        suffix_name = ""
    else:
        #Log
        print(f"[OK] Terapia trovata: {terapia}")
        if not utils.verifica_terapia(terapia):
            # Log
            print(f"[ERRORE] Terapia non valida: {terapia}")
            # il messaggio da dare al t2s
            # print("La terapia fornita non è valida")
            return
        # Se la terapia è valida, applicala
        # Nota: la funzione applica_terapia è commentata gestisce gli errori non internamente
        day_data = utils.applica_terapia(day_data, terapia)
        # try:
        #     day_data = utils.applica_terapia(day_data, terapia)
        # except Exception as e:
        #     print(f"{e}")
        #     return
        suffix_name = f"{terapia['text']}" 

    replay_results = utils.replay(patient_info, day_data, save_name, suffix_name, SAVE_FOLDER)
    if not replay_results:
        #Log
        print(
            f"[ERRORE] Replay della terapia fallito per {paziente} per il giorno {data}."
        )
        # il messaggio da dare al t2s
        # print(f"Replay della terapia fallito per {paziente} per il giorno {data}.")
        return
    #Log
    print(f"[OK] Replay della terapia completato per {paziente} per il giorno {data}.")
    # il messaggio da dare al t2s
    # print(f"Simulazione della terapia completato per {paziente} per il giorno {data}.")

def analizza(result_json):
    from py_replay_bg.analyzer import Analyzer
    import pickle
    #log
    print(f"[ANALIZZA] Intent: {result_json.get('intent')}")
    paziente = result_json.get("paziente")
    data = result_json.get("data")
    terapia = result_json.get("terapia")

    if terapia is None or not utils.verifica_terapia(terapia):
        #Log
        print(f"[ERRORE] Terapia non valida o mancante: {terapia}")
        # il messaggio da dare al t2s
        # print("La terapia fornita non è valida o mancante.")
        return

    text = terapia.get("text")
    if not text:
        #Log
        print(f"[ERRORE] Campo 'text' mancante nella terapia: {terapia}")
        return

    filepath = os.path.join(SAVE_FOLDER, 'results', 'workspaces', f'{paziente}_{data}{text}.pkl')
    if not os.path.exists(filepath):
        #Log
        print(f"[ERRORE] File dei risultati non trovato: {filepath}")
        # il messaggio da dare al t2s
        # print(f"Simulazione non trovata per {paziente} per il giorno {data}.")
        return

    with open(filepath, 'rb') as file:
        replay_results = pickle.load(file)

    if not replay_results:
        #Log
        print(f"[ERRORE] Replay results non trovati per {paziente} per il giorno {data}.")
        # il messaggio da dare al t2s
        # print(f"Simulazione non trovata per {paziente} per il giorno {data}.")
        return

    analysis = Analyzer.analyze_replay_results(replay_results)
    # Log
    print(f"[ANALISI] Completata per  per {paziente} per il giorno {data} con terapia {text}.")
    # print(f"[ANALISI RISULTATI] {analysis}")
    return utils.stampa_analisi(analysis,text)

def confronta(result_json):
    # Log
    print(f"[CONFRONTA] Intent: {result_json.get('intent')}")

    paziente = result_json.get("paziente")
    data = result_json.get("data")
    terapie = result_json.get("terapia")  # Lista di 2 terapie

    if not isinstance(terapie, list) or len(terapie) < 2:
        #Log
        print(f"[ERRORE] Devi fornire almeno due terapie nel campo 'terapia'. Ricevuto: {terapie}")
        # il messaggio da dare al t2s
        # print("Devi fornire almeno due terapie.")
        return

    risultati = []
    for terapia in terapie:
        if not utils.verifica_terapia(terapia):
            #Log
            print(f"[ERRORE] Terapia non valida: {terapia}")
            # il messaggio da dare al t2s
            # print("La terapia fornita non è valida.")
            return
        input_singolo = {
            "intent": "analizza",
            "paziente": paziente,
            "data": data,
            "terapia": terapia
        }
        risultato = analizza(input_singolo)
        if not risultato:
            #Log
            print(f"[ERRORE] Analisi fallita per terapia: {terapia}")
            # il messaggio da dare al t2s
            # print(f"Analisi fallita per la terapia")
            return

        # risultato è dict, trasformiamolo in testo
        testo = utils.formatta_analisi_testo(risultato)
        risultati.append(testo)

    return "\n\n".join(risultati)




def parse_output(result_json):
    intent = result_json.get("intent")

    if intent == "crea_utente":
        crea_paziente(result_json)
    elif intent == "crea_dt":
        return crea_dt(result_json)
    elif intent == "simula_dt":
        return simula_dt(result_json)
    elif intent == "analizza":
        return analizza(result_json)
    elif intent == "confronta":
        return confronta(result_json)
    else:
        #Log
        print(f"[ERRORE] Intent sconosciuto: {intent}")
        # il messaggio da dare al t2s
        # print("é stato fornito un comando sconosciuto.")

# app.py
import traceback
from bottle import route, run, template, request, static_file, HTTPResponse, response
import json
import uuid
from py_replay_bg.py_replay_bg import ReplayBG
from py_replay_bg.analyzer import Analyzer
import utils
from threading import Thread

# Dizionario globale per tenere traccia dei job
JOB_STATUS = {}

# Funzione di risposta in caso di errore
def error_response(status_code, message):
    body = json.dumps({"status": "error", "message": message})
    return HTTPResponse(status=status_code, body=body, content_type="application/json")

#Funzione per la simulazione del twin in modo asincrono
def replay_twin_async(dati_paziente, dati_ottimizzazione_modello, save_name, suffix_name, job_id, titolo = "base"):
    try:
        JOB_STATUS[job_id] = {"state": "in_progress", "message": "Simulazione Digital Twin in corso..."}

        # Esegui la simulazione
        replay_results = utils.replay(dati_paziente, dati_ottimizzazione_modello, save_name, suffix_name)

        # Esegui l'analisi dei risultati
        analysis = Analyzer.analyze_replay_results(replay_results, data=dati_ottimizzazione_modello)
        
        json_results = {
            "titolo": titolo,
            "mean_glucose": f"{analysis['median']['glucose']['variability']['mean_glucose']}",
            "std_deviation": f"{analysis['median']['glucose']['variability']['std_glucose']}",
            "tir": f"{analysis['median']['glucose']['time_in_ranges']['time_in_target']}",
            "time_in_hypoglycemia": f"{analysis['median']['glucose']['time_in_ranges']['time_in_hypoglycemia']}",
            "time_in_hyperglycemia": f"{analysis['median']['glucose']['time_in_ranges']['time_in_hyperglycemia']}"
        }
      
        #TODO Stampa i risultati piuttosto che restituirli cosi dato che analysys sembra non serializzabile. oppure crea un diz a partire da essi
        JOB_STATUS[job_id] = {
            "state": "done",
            "message": "Simulazione e analisi completate con successo",
            "analysis": json_results
        }
        
    except Exception as e:
        JOB_STATUS[job_id] = {
            "state": "error",
            "message": "Errore nella simulazione o nell'analisi",
            "details": str(e),
        }
        
def crea_twin_async(dati_paziente, dati_ottimizzazione_modello, save_name, job_id):
    try:
        # Inizializza lo stato del job come "in_progress"
        JOB_STATUS[job_id] = {"state": "in_progress", "message": "Creazione Digital Twin in corso..."}

        # Avvia la creazione del twin
        utils.twin(dati_paziente, dati_ottimizzazione_modello, save_name)

        # Quando il processo è finito correttamente
        JOB_STATUS[job_id] = {"state": "done", "message": "Twin creato con successo"}
    except Exception as e:
        # In caso di errore, memorizza l'errore nello stato del job
        JOB_STATUS[job_id] = {
            "state": "error",
            "message": "Errore nella creazione del Twin",
            "details": str(e),
        }
        
#Messaggio SImulazione dt avviata anche se questa route da errire
@route("/status/<job_id>")
def status(job_id):
    # Controlla se il job_id esiste nel dizionario JOB_STATUS
    job_state = JOB_STATUS.get(job_id)

    if job_state is None:
        return error_response(404, "Job non trovato")

    return json.dumps(job_state)


@route("/crea_dt", method="POST")
def crea_dt():
    dati_paziente_file = request.files.get("dati_paziente")
    dati_ottimizzazione_modello_file = request.files.get("dati_ottimizzazione_modello")
    nome_nuovo_dt = request.forms.get("nome_nuovo_dt")

    # Validazione input
    if not dati_paziente_file:
        return error_response(400, "File 'dati_paziente' non trovato")
    if not dati_ottimizzazione_modello_file:
        return error_response(400, "File 'dati_ottimizzazione_modello' non trovato")
    if not nome_nuovo_dt:
        return error_response(400, "Nome nuovo digital twin mancante")

    # Parsing file
    try:
        dati_paziente = utils.load_patient_info(dati_paziente_file.file)
        print(dati_paziente)
        dati_ottimizzazione_modello = utils.load_test_data(
            dati_ottimizzazione_modello_file.file
        )
    except Exception as e:
        return error_response(422, f"Errore nel parsing dei file: {e}")

    # Generazione job_id
    job_id = str(uuid.uuid4())
    save_name_unico = f"{nome_nuovo_dt}"

    # Avvio del processo in background
    try:
        t = Thread(
            target=crea_twin_async,
            args=(dati_paziente, dati_ottimizzazione_modello, save_name_unico, job_id),
        )
        t.daemon = True
        t.start()
    except Exception as e:
        return error_response(500, f"Errore interno nell'avvio del processo: {e}")

    # Risposta asincrona con job_id
    response.content_type = "application/json"
    return json.dumps(
        {
            "status": "in_progress",
            "job_id": job_id,
            "message": "Creazione del Digital Twin avviata",
        }
    )

#Ora creiamo la route replay_dt, che accetta da formdata: il nome del dt (nome_dt) e lo scenario (scenario)
@route("/replay_dt", method="POST")
def replay_dt():
    dati_paziente_file = request.files.get("dati_paziente")
    dati_ottimizzazione_modello_file = request.files.get("dati_ottimizzazione_modello")
    nome_dt = request.forms.get("nome_dt")
    scenario = request.forms.get("scenario")
    
    # Validazione input
    if not dati_paziente_file:
        return error_response(400, "File 'dati_paziente' non trovato")
    if not dati_ottimizzazione_modello_file:
        return error_response(400, "File 'dati_ottimizzazione_modello' non trovato")
    if not nome_dt:
        return error_response(400, "Nome del digital twin mancante")
    if not scenario:
        return error_response(400, "Scenario mancante")
    
    # Parsing file
    try:
        dati_paziente = utils.load_patient_info(dati_paziente_file.file)
        print(dati_paziente)
        dati_ottimizzazione_modello = utils.load_test_data(
            dati_ottimizzazione_modello_file.file
        )
    except Exception as e:
        return error_response(422, f"Errore nel parsing dei file: {e}")

    if scenario == "base":
        titolo = "Simulazione con gli stessi dati del twinning"
        suffix_name = "_base"
    elif scenario == "bolo30meno":
        titolo = "Simulazione con bolo ridotto del 30%"
        suffix_name = "_bolo30meno"
        dati_ottimizzazione_modello["bolus"] = dati_ottimizzazione_modello["bolus"] * 0.7
    else:
        return error_response(400, "Scenario non valido")
    # Generazione job_id
    job_id = str(uuid.uuid4())
    save_name_unico = f"{nome_dt}"
    
    # Avvio del processo in background
    try:
        t = Thread(
            target=replay_twin_async,
            args=(dati_paziente, dati_ottimizzazione_modello, save_name_unico, suffix_name, job_id, titolo)
        )
        t.daemon = True
        t.start()
    except Exception as e:
        return error_response(500, f"Errore interno nell'avvio del processo: {e}")

    # Risposta asincrona con job_id
    response.content_type = "application/json"
    return json.dumps(
        {
            "status": "in_progress",
            "job_id": job_id,
            "message": "Simulazione del Digital Twin avviata",
        }
    )
    
    
@route("/")
def index():
    return template("index.tpl")


@route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="static")


run(host="localhost", server="paste", port=8080, debug=True, reloader=True)

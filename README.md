# pyreplaybg_demo

Questa demo mostra il funzionamento di **`py_replay_bg`**, un'implementazione Python del sistema `ReplayBg`, attraverso una webapp sviluppata con il micro-framework [Bottle](https://bottlepy.org/).

## 🚀 Obiettivo

Simulare un **Digital Twin (DT)** per la gestione della glicemia, in due fasi principali:

1. Creazione del digital twin a partire da dati reali.
2. Simulazione predittiva su scenari glicemici possibili.

---

## ⚙️ Requisiti

- [Anaconda](https://www.anaconda.com/products/distribution) o [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installato sul sistema.

---

## 🛠️ Installazione

### 1. Clonare il repository

```bash
git clone https://github.com/tuo-username/pyreplaybg_demo.git
cd pyreplaybg_demo
```

### 2. Creare l'environment Conda

```bash
conda env create -f environment.yml
```

### 3. Attivare l'environment

```bash
conda activate tirocinio
```

---

## ▶️ Esecuzione

Per avviare la webapp:

```bash
python app.py
```

Verrà lanciato un server embedded accessibile all’indirizzo:

```
http://localhost:8080
```

Il browser si aprirà automaticamente con la pagina iniziale dell'app.

---

## 🧪 Flusso della WebApp

Una volta aperta l’interfaccia nel browser, l’utente viene guidato attraverso i seguenti passaggi:

### **1. Creazione del Digital Twin**

- Caricare il file **`patient_info.csv`** con le informazioni del paziente.
- Caricare il file **`data_day_1.csv`** contenente i dati relativi al giorno da simulare.
- Premere il pulsante per **generare il Digital Twin**.

### **2. Simulazione**

- Selezionare una delle **due simulazioni disponibili**.
- Avviare la simulazione.
- Attendere l’elaborazione e **visualizzare i risultati** prodotti, che verranno salvati nella cartella `results/`.

---

## 📁 Struttura del progetto

```
pyreplaybg_demo/
├── __pycache__/             # File cache Python
├── results/                 # Output delle simulazioni
├── static/                  # Risorse statiche (CSS, immagini, JS)
├── views/                   # Template HTML per la UI
├── app.py                   # Avvia il server e gestisce la logica Bottle
├── utils.py                 # Funzioni di supporto
├── environment.yml          # Definizione dell'environment Conda (include pip)
├── patient_info.csv         # Esempio di input paziente
├── data_day_1.csv           # Esempio di dati giornalieri
└── README.md
```

---

## 📌 Note

- L’environment `tirocinio` include pacchetti installati sia tramite `conda` che `pip`, già raccolti in `environment.yml`.
- È importante mantenere la struttura delle cartelle per il corretto funzionamento della webapp.
- I file `.csv` forniti sono esempi minimi per test e dimostrazione.

---

## 👤 Autore

Andrea

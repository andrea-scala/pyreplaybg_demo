import pandas as pd
import os
import io
from py_replay_bg.py_replay_bg import ReplayBG

SAVE_FOLDER = os.path.abspath("")


def replay(dati_paziente, dati_ottimizzazione_modello, save_name, suffix_name):
    # Inizializza ogetto ReplayBG
    rbg = ReplayBG(
        SAVE_FOLDER,
        blueprint="multi-meal",
        yts=5,
        exercise=False,
        seed=1,
        plot_mode=True,
        verbose=True,
    )

    patient_row = dati_paziente[dati_paziente["patient"] == 1].iloc[0]
    bw = float(patient_row["bw"])  # Body weight

    return rbg.replay(
        data=dati_ottimizzazione_modello,
        bw=bw,
        save_name=save_name,
        twinning_method="map",
        save_workspace=True,
        save_suffix=suffix_name,
    )


def twin(dati_paziente, dati_ottimizzazione_modello, save_name):
    # Inizializza ogetto ReplayBG
    rbg = ReplayBG(
        SAVE_FOLDER,
        blueprint="multi-meal",
        yts=5,
        exercise=False,
        seed=1,
        plot_mode=True,
        verbose=True,
    )

    patient_row = dati_paziente[dati_paziente["patient"] == 1].iloc[0]
    bw = float(patient_row["bw"])  # Body weight
    u2ss = float(patient_row["u2ss"])

    # Media dell'infusione basale di insulina del paziente
    # print("bw", bw)
    # print("u2ss", u2ss)

    # for x, y in dati_ottimizzazione_modello.items():
    #     print(x, y)

    # Generazione del twin
    rbg.twin(
        dati_ottimizzazione_modello,
        bw=bw,
        save_name=save_name,
        twinning_method="map",
        parallelize=True,
        u2ss=u2ss,
    )
    return True


def load_patient_info(file):
    df = pd.read_csv(file)
    return df


def load_test_data(file):
    df = pd.read_csv(file)
    df.t = pd.to_datetime(df["t"])
    return df


def show_data(data):
    for row in data.itertuples(index=True):
        print(
            f"i: {row.Index}, t: {row.t}, bolus: {row.bolus}, meal: {row.meal}, basal: {row.basal}, exercise: {row.exercise}, bg: {row.bg}"
        )

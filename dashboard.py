import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configurazione della pagina
st.set_page_config(page_title="Zero-Day Anomaly Detection", layout="wide")

st.title("🛡️ Dashboard Operativa: Rilevamento Attacchi Zero-Day")
st.markdown("Monitoraggio delle anomalie di rete tramite Autoencoder. I dati sono caricati direttamente dai risultati di inferenza del modello PyTorch.")

# 1. Caricamento Dati
@st.cache_data
def load_data():
    with open("dashboard_data.json", "r") as f:
        return json.load(f)

try:
    data = load_data()
except FileNotFoundError:
    st.error("File 'dashboard_data.json' non trovato. Eseguire il Jupyter Notebook")
    st.stop()

# Estrazione metriche
tau = data["tau"]
auc = data["auc"]
dr = data["dr"]
far = data["far"]
mse_list = data["mse"]
labels_list = data["labels"]

# Mostra i KPI (Key Performance Indicators) in cima
st.header("Metriche di Riferimento del Modello")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Soglia di Rilevamento (τ)", f"{tau:.5f}")
col2.metric("AUC", f"{auc:.4f}")
col3.metric("Detection Rate (DR)", f"{dr}%", "+ Target >95%")
col4.metric("False Alarm Rate (FAR)", f"{far}%", "- Target <5%", delta_color="inverse")

st.divider()

# Preparazione dei dati simulati
df = pd.DataFrame({
    "MSE (Errore Ricostruzione)": mse_list,
    "Label Reale": ["Attacco" if l == 1 else "Benigno" for l in labels_list]
})

# Classificazione basata sulla soglia tau calcolata dinamicamente
df["Predizione del Modello"] = df["MSE (Errore Ricostruzione)"].apply(
    lambda x: "🚨 MINACCIA ZERO-DAY" if x > tau else "✅ Normale"
)

# Verifica se la previsione del modello è corretta o errata
df["Esito Classificazione"] = np.where(
    ((df["Label Reale"] == "Attacco") & (df["MSE (Errore Ricostruzione)"] > tau)) | 
    ((df["Label Reale"] == "Benigno") & (df["MSE (Errore Ricostruzione)"] <= tau)),
    "Corretto", "Errato"
)

# Tabella Dettagliata
st.header("🔍 Dettaglio Traffico di Rete Analizzato")
st.markdown("Visualizza l'esito di ogni pacchetto. Gli errori del modello sono evidenziati nella tabella.")

# Per evidenziare in rosso gli errori nella tabella
def color_errors(val):
    color = '#ffcccc' if val == 'Errato' else ''
    return f'background-color: {color}'

styled_df = df.style.map(color_errors, subset=['Esito Classificazione'])
st.dataframe(styled_df, use_container_width=True, height=400)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import streamlit as st

# Charger les données
@st.cache_data
def load_data():
    df = pd.read_csv("data/1h-attack-log.csv",sep=",",names=["ipsrc","ipdst","portdst","proto","action","date","regle"])
    return df

df = load_data()

# Affichage des premières lignes
title = "🔍 Détection d’anomalies"
st.title(title)
st.write("Exploration et détection d'anomalies dans les logs réseau.")

# Sélection des attributs utiles (à adapter selon le fichier de log)
time_col = "date"  # Adapter au fichier
df[time_col] = pd.to_datetime(df[time_col])

# Détection des IPs suspectes (DDoS)
st.subheader("📌 Détection d’attaques DDoS")
# Widgets pour ajuster les seuils
seuil = st.slider("Seuil minimum de requêtes pour prise en compte :", min_value=1, max_value=100, value=95)
ip_counts = df['ipsrc'].value_counts()
thresh = np.percentile(ip_counts, seuil)
ddos_ips = ip_counts[ip_counts > thresh].index.tolist()
st.write(f"Seuil de détection ({seuil}e percentile) : {thresh:.0f} requêtes")
st.write(f"Nombre d'IPs suspectes : {len(ddos_ips)}")
st.write(ip_counts[ip_counts > thresh])

# Clustering des IPs suspectes
st.subheader("📌 Clustering des IPs selon leur comportement")
if len(ddos_ips) > 2:
    df_ddos = df[df['ipsrc'].isin(ddos_ips)][['ipsrc', 'ipdst', 'portdst']]
    df_ddos['ipsrc'] = df_ddos['ipsrc'].astype('category').cat.codes
    df_ddos['ipdst'] = df_ddos['ipdst'].astype('category').cat.codes

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_ddos)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df_ddos['cluster'] = kmeans.fit_predict(X_scaled)
    
    fig, ax = plt.subplots()
    sns.scatterplot(x=df_ddos['ipsrc'], y=df_ddos['ipdst'], hue=df_ddos['cluster'], palette="viridis", ax=ax)
    ax.set_xlabel("Source IP")
    ax.set_ylabel("Destination IP")
    st.pyplot(fig)
else:
    st.write("Pas assez d'IP suspectes pour faire un clustering.")
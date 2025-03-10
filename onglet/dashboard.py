import pandas as pd 
import streamlit as st
import plotly.express as px
import ipinfo

st.title("Dashboard")

# Charger les données
df = pd.read_csv("data/1h-attack-log.csv",sep=",",names=["ipsrc","ipdst","portdst","proto","action","date","regle"])

# Ajouter les colonnes latitude et longitude
# access_token = 'YOUR_IPINFO_ACCESS_TOKEN'
# handler = ipinfo.getHandler(access_token)

# def get_lat_lon(ip):
#     details = handler.getDetails(ip)
#     return details.latitude, details.longitude

# df[['latitude', 'longitude']] = df['ipsrc'].apply(lambda ip: pd.Series(get_lat_lon(ip)))

# Nombre total de connexions enregistrées
total_connections = len(df)
st.metric("Nombre total de connexions enregistrées", total_connections)

# Ratio des connexions acceptées/rejetées
accepted_connections = df[df['action'] == 'Permit']
rejected_connections = df[df['action'] == 'Deny']
ratio_accepted_rejected = len(accepted_connections) / len(rejected_connections)
st.metric("Ratio des connexions acceptées/rejetées", ratio_accepted_rejected)

# Top 5 des IPs sources les plus actives
top_5_ips = df['ipsrc'].value_counts().head(5)
st.subheader("Top 5 des IPs sources les plus actives")
st.write(top_5_ips)

# Top 10 des ports les plus utilisés
filtered_ports = df[(df['portdst'] < 1024) & (df['action'] == 'Permit')]
top_10_ports = filtered_ports['portdst'].value_counts().head(10)
st.subheader("Top 10 des ports inférieurs à 1024 avec un accès autorisé")
st.write(top_10_ports)

# Nombre de tentatives d'accès non autorisées
unauthorized_access_attempts = len(df[df['action'] == 'deny'])
st.metric("Nombre de tentatives d'accès non autorisées", unauthorized_access_attempts)

# Graphique en camembert : Proportion des connexions acceptées vs refusées
status_counts = df['action'].value_counts()
fig_pie = px.pie(values=status_counts, names=status_counts.index, title="Proportion des connexions acceptées vs refusées")
st.plotly_chart(fig_pie)

# Bar chart : Top 10 des ports les plus utilisés
fig_bar = px.bar(top_10_ports, x=top_10_ports.index, y=top_10_ports.values, title="Top 10 des ports les plus utilisés")
st.plotly_chart(fig_bar)

# Carte interactive : Localisation des IP sources des connexions
# fig_map = px.scatter_geo(df, lat='latitude', lon='longitude', hover_name='ipsrc', title="Localisation des IP sources des connexions")
# st.plotly_chart(fig_map)
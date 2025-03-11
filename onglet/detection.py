from analyses import fonctions as func
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import streamlit as st
import plotly.graph_objects as go
import networkx as nx

# Charger les données
df = func.get_data()
df["portdst"] = pd.to_numeric(df["portdst"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
# st.dataframe(df.head())
# Affichage des premières lignes
title = "🔍 Détection d’anomalies"
st.title(title)
st.write("Exploration et détection d'anomalies dans les logs réseau.")

# Détection des IPs suspectes (DDoS)
st.subheader("📌 Détection d’attaques DDoS")
seuil = st.slider("Seuil minimum de requêtes pour prise en compte :", min_value=95, max_value=100, value=99)
ip_counts = df['ipsrc'].value_counts()
thresh = np.percentile(ip_counts, seuil)
ddos_ips = ip_counts[ip_counts > thresh].index.tolist()
st.write(f"Seuil de détection ({seuil}e percentile) : {thresh:.0f} requêtes")
st.write(f"Nombre d'IPs suspectes : {len(ddos_ips)}")
st.write(ip_counts[ip_counts > thresh])

# Clustering des IPs suspectes
# Interface pour lancer le clustering
st.subheader("📌 Clustering des IPs selon leur comportement")
k_clusters = st.slider("Nombre de clusters (K-Means) :", min_value=2, max_value=10, value=3)
if st.button("Lancer le clustering"):
    if len(ddos_ips) >= k_clusters:
        df_ddos = df[df['ipsrc'].isin(ddos_ips)].copy()
        df_ddos['ipsrc_orig'] = df_ddos['ipsrc']
        df_ddos['ipdst_orig'] = df_ddos['ipdst']

        df_ddos['ipsrc'] = df_ddos['ipsrc'].astype('category').cat.codes
        df_ddos['ipdst'] = df_ddos['ipdst'].astype('category').cat.codes

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_ddos[['ipsrc', 'ipdst', 'portdst']])

        kmeans = KMeans(n_clusters=k_clusters, random_state=42)
        df_ddos['cluster'] = kmeans.fit_predict(X_scaled)

        # Création du graphe avec NetworkX
        G = nx.Graph()

        for _, row in df_ddos.iterrows():
            G.add_node(row['ipsrc_orig'], label=row['ipsrc_orig'], cluster=row['cluster'])
            G.add_node(row['ipdst_orig'], label=row['ipdst_orig'], cluster=row['cluster'])
            G.add_edge(row['ipsrc_orig'], row['ipdst_orig'])

        pos = nx.spring_layout(G, dim=3, seed=42)
        x_nodes, y_nodes, z_nodes, colors, hover_texts = [], [], [], [], []

        for node in G.nodes():
            x_nodes.append(pos[node][0])
            y_nodes.append(pos[node][1])
            z_nodes.append(pos[node][2])
            colors.append(G.nodes[node]['cluster'])
            hover_texts.append(G.nodes[node]['label'])

        edge_x, edge_y, edge_z = [], [], []
        for edge in G.edges():
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_z.extend([z0, z1, None])

        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(color='gray', width=1), hoverinfo='none'))
        fig.add_trace(go.Scatter3d(x=x_nodes, y=y_nodes, z=z_nodes, mode='markers', marker=dict(size=5, color=colors, colorscale='Viridis', opacity=0.8), text=hover_texts, hoverinfo='text', name="IPs"))
        
        fig.update_layout(
            title="Graphe 3D des connexions IP (Clustering)",
            scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z", xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), zaxis=dict(showgrid=False, zeroline=False, showticklabels=False)),
            margin=dict(l=0, r=0, b=0, t=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("📌 Caractérisation des clusters")
        cluster_summary = df_ddos.groupby('cluster').agg(
            nb_ipsrc=('ipsrc_orig', 'nunique'),
            nb_ipdst=('ipdst_orig', 'nunique'),
            avg_portdst=('portdst', 'mean'),
            proportion_deny=('action', lambda x: (x == 'DENY').mean())
        ).reset_index()
        st.write("Résumé des caractéristiques des clusters :")
        st.dataframe(cluster_summary)        
    else:
        st.write("Pas assez d'IP suspectes pour faire un clustering.")

# selected_cluster = st.selectbox(
#     "Sélectionnez un cluster pour voir les IPs associées :",
#     cluster_summary['cluster'].unique()
# )

# unique_ips = df_ddos[df_ddos['cluster'] == selected_cluster]['ipsrc_orig'].unique()
# st.subheader(f"📌 IPs uniques du cluster {selected_cluster}")
# st.dataframe(pd.DataFrame(unique_ips, columns=["IPs uniques"]))
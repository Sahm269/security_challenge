import pandas as pd 
import streamlit as st
import plotly.express as px
import ipaddress
import plotly.graph_objects as go

st.title("Dashboard")

# Charger les données
df = pd.read_csv("data/1h-attack-log.csv",sep=",",names=["ipsrc","ipdst","portdst","proto","action","date","regle"])

# # Comptage des actions par IP source
# df_counts = df.groupby(["ipsrc", "action"]).size().reset_index(name="count")

# # Sélection des 5 IPs sources les plus actives
# top_5_ips = df["ipsrc"].value_counts().head(5).index
# df_top5 = df_counts[df_counts["ipsrc"].isin(top_5_ips)]

# df_counts = df.groupby(["ipsrc"]).size().reset_index(name="count")

# # Sélection des 5 IPs sources les plus actives
# top_5_ips = df["ipsrc"].value_counts().head(5).index
# df_top5 = df_counts[df_counts["ipsrc"].isin(top_5_ips)]


# # Affichage du graphique dans Streamlit
# st.subheader("Top 5 des IP Source les plus émetteuses")

# fig = px.bar(df_top5.sort_values(by="count", ascending=False), 
#              x="ipsrc", 
#              y="count", 
#              barmode="group",
#              labels={"ipsrc": "IP Source", "count": "Nombre d'actions"},
#              text="count"
# )

# st.plotly_chart(fig)


top_5_ips = df['ipsrc'].value_counts().head(5)
st.subheader("Top 5 des IPs sources les plus actives")
fig_top5 = px.bar(top_5_ips, 
                  x=top_5_ips.index, 
                  y=top_5_ips.values, 
                  labels={'x': 'IP Source', 'y': 'Nombre de connexions'},
                  text=top_5_ips.values
)
st.plotly_chart(fig_top5)


st.subheader("Pourcentage d'actions Deny pour les 5 IP source les plus actives")

# Comptage des actions par IP source
df_counts = df.groupby(["ipsrc", "action"]).size().reset_index(name="count")

# Sélection des 5 IPs sources les plus actives
top_5_ips = df["ipsrc"].value_counts().head(5).index

df_top5 = df_counts[df_counts["ipsrc"].isin(top_5_ips)]


# calculer le pourcentage de deny par ip source
df_top5 = df_top5.reset_index(drop=True)
df_top5['percent'] = df_top5.groupby('ipsrc')['count'].apply(lambda x: x / x.sum() * 100).values

# Sort par ip filtrer pour uniquement que les deny
df_top5 = df_top5[df_top5['action'] == 'Deny']
df_top5 = df_top5.sort_values(by='ipsrc')

fig3 = px.line_polar(df_top5, r='percent', theta='ipsrc', line_close=True)
fig3.update_traces(fill='toself')


fig3.update_layout(
    polar=dict(
        radialaxis=dict(
            tickfont=dict(size=14, family='Arial', color='black', weight='bold'),  # Police en gras et en noir
        )
    )
)

st.plotly_chart(fig3)

# Sélection des 5 IPs sources les plus actives
top_5_ips = df["ipsrc"].value_counts().head(5).index

# Filtrer le DataFrame pour obtenir les lignes correspondantes aux IPs sources
df_top5 = df[df["ipsrc"].isin(top_5_ips)]

# Filtrer les IPs destination (ipdst) qui ne sont pas dans les 5 IPs sources les plus actives
df_top5_dest = df_top5[~df_top5["ipdst"].isin(top_5_ips)]

# Créer un DataFrame pour les flux (source, destination, et le nombre d'occurrences)
flow_data = df_top5_dest.groupby(["ipsrc", "ipdst"]).size().reset_index(name="count")

# Créer un dictionnaire pour les noeuds (IPs source et destination)
nodes = pd.concat([flow_data["ipsrc"], flow_data["ipdst"]]).unique()
node_dict = {node: i for i, node in enumerate(nodes)}

# Créer les liens pour le Sankey
links = flow_data.apply(lambda row: {
    "source": node_dict[row["ipsrc"]],
    "target": node_dict[row["ipdst"]],
    "value": row["count"]
}, axis=1).tolist()

# Préparer la figure Sankey
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,  # Espace autour des noeuds
        thickness=20,  # Largeur des noeuds
        line=dict(color="black", width=0.5),  # Bordure des noeuds
        label=nodes  # Labels des noeuds
    ),
    link=dict(
        source=[link["source"] for link in links],
        target=[link["target"] for link in links],
        value=[link["value"] for link in links],
        color="blue"  # Couleur des liens
    )
))

# Affichage du graphique dans Streamlit
st.subheader("Graphique Sankey des flux entre IP Source et IP Destination")
st.plotly_chart(fig)

# Top 10 des ports les plus utilisés
filtered_ports = df[(df['portdst'] < 1024) & (df['action'] == 'Permit')]
top_10_ports = filtered_ports['portdst'].value_counts().head(10)
# Créer un DataFrame à partir de top_10_ports
df_top_10_ports = top_10_ports.reset_index()

# Renommer les colonnes
df_top_10_ports.columns = ['portdst', 'count']

# print(df_top_10_ports)

df_top_10_ports = df_top_10_ports.sort_values(by='portdst')

# change type portdst à str
df_top_10_ports['portdst'] = df_top_10_ports['portdst'].astype(str)

# Ajouter le suffixe port devant chaque valeur de portdst 
df_top_10_ports['portdst'] = df_top_10_ports['portdst'].apply(lambda x: 'port '+ x)

# Sort le df 
df_top_10_ports = df_top_10_ports.sort_values(by='count', ascending=True)

print(df_top_10_ports)
# Afficher le DataFrame
st.subheader("Top 10 des ports inférieurs à 1024 avec un accès autorisé")
fig_10 = px.bar(df_top_10_ports,
                x='count', 
                y=df_top_10_ports['portdst'], 
                orientation='h',
                labels={'y': 'Port', 'count': 'Nombre de connexions'},
                text='count'
)
st.plotly_chart(fig_10)


# Trier df par portdst
df_top_10_ports = df_top_10_ports.sort_values(by='portdst')

# change type portdst à str
df_top_10_ports['portdst'] = df_top_10_ports['portdst'].astype(str)

# Ajouter le suffixe port devant chaque valeur de portdst 
df_top_10_ports['portdst'] = df_top_10_ports['portdst'].apply(lambda x: 'port '+ x)

# Remove le port 80 
df_top_10_ports = df_top_10_ports[df_top_10_ports['portdst'] != 'port 80']


# Afficher le texte de Theta en noir et en gras
fig2 = px.line_polar(df_top_10_ports, r='count', theta='portdst', line_close=True)
fig2.update_traces(fill='toself')

fig2.update_layout(
    polar=dict(
        radialaxis=dict(
            tickfont=dict(size=14, family='Arial', color='black', weight='bold'),
        )
    )
)

st.plotly_chart(fig2)

# Nombre de connexions Deny par jour
df['date'] = pd.to_datetime(df['date'])
df['day'] = df['date'].dt.date
deny_connections = df[df['action'] == 'Deny'].groupby('day').size().reset_index(name='count')
st.subheader("Nombre de connexions Deny par jour")
fig_deny = px.line(deny_connections, x='day', y='count', labels={'day': 'Date', 'count': 'Nombre de connexions Deny'}, title="Nombre de connexions Deny par jour")
st.plotly_chart(fig_deny)



# Plan d'adressage de l'Université
university_ip_ranges = [
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('159.84.0.0/16'),
    ipaddress.ip_network('10.70.0.0/16'),
]

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_university_ip(ip):
    if not is_valid_ip(ip):
        return False
    ip_addr = ipaddress.ip_address(ip)
    return any(ip_addr in network for network in university_ip_ranges)

# Filtrer les adresses IP invalides
df = df[df['ipsrc'].apply(is_valid_ip)]

# Lister les accès des adresses non incluses dans le plan d'adressage de l'Université
non_university_accesses = df[~df['ipsrc'].apply(is_university_ip)]
st.subheader("Accès des adresses non incluses dans le plan d'adressage de l'Université")
st.write(non_university_accesses)


st.title("Analyse des IP sources et destinations")

# Calculer le nombre total de connexions par IP source, action et IP destination
df_count = df.groupby(['ipsrc', 'action', 'ipdst']).size().reset_index(name='total_connections')

# Ajouter un curseur pour filtrer les données en fonction du nombre total de connexions
min_conn, max_conn = df_count['total_connections'].min(), df_count['total_connections'].max()
selected_range = st.slider("Sélectionnez la plage de connexions totales", min_conn, max_conn, (min_conn, max_conn))

# Filtrer les données en fonction de la plage sélectionnée
filtered_df_count = df_count[(df_count['total_connections'] >= selected_range[0]) & (df_count['total_connections'] <= selected_range[1])]

fig_slider = px.scatter(filtered_df_count, x="ipsrc", y="total_connections", color="action",
                        symbol="action", 
                        symbol_map={"Permit": "circle", "Deny": "cross"},
                        color_discrete_map={"Permit": "blue", "Deny": "red"},
                        title="Nombre total de connexions par IP source et action",
                        labels={"ipsrc": "IP Source", "total_connections": "Nombre total de connexions", "action": "Action"},
                        hover_data={"ipdst": "IP Dest"})

fig_slider.update_xaxes(tickangle=270)

st.plotly_chart(fig_slider)




# Sélecteur interactif pour choisir une IP source
selected_ipsrc = st.selectbox("Sélectionnez une IP source :", df['ipsrc'].unique())

# Filtrer les données pour l'IP sélectionnée
df_filtered = df[df['ipsrc'] == selected_ipsrc]

# Ajouter un comptage des connexions pour chaque ipdst et action
df_grouped = df_filtered.groupby(['ipdst', 'action']).size().reset_index(name='Count')

# Création du scatter plot
fig_scatter = px.scatter(
    df_grouped,
    x='ipdst',
    y='Count',
    color='action',  # Couleur en fonction de Permit/Deny
    symbol='action',  # Différentes formes en fonction de Permit/Deny
    color_discrete_map={'Permit': 'blue', 'Deny': 'red'},  # Bleu pour Permit, Rouge pour Deny
    symbol_map={'Permit': 'circle', 'Deny': 'cross'},  # Cercle pour Permit, Croix pour Deny
    title=f"Connexions vers IP destination depuis {selected_ipsrc}",
    labels={'ipdst': 'IP destination', 'Count': 'Nombre de connexions'}
)

# Affichage du graphique
st.plotly_chart(fig_scatter)



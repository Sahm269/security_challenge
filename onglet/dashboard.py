from analyses import fonctions as func
import pandas as pd 
import streamlit as st
import plotly.express as px
import ipaddress
import plotly.graph_objects as go

st.markdown("""
    <h1 style="font-size: 36px; color: #4bcfd1; text-align: center; font-family: 'Arial', sans-serif;">
        📊 <span style="font-weight: bold;">Dashboard</span> 📊
    </h1>
    <p style="font-size: 18px; color: #a8e5e4; text-align: center; font-family: 'Arial', sans-serif;">
        Analyse de différentes métriques pour les IPs et les ports.
    </p>
""", unsafe_allow_html=True)
# Charger les données
#df = pd.read_csv("data/1h-attack-log.csv",sep=",",names=["ipsrc","ipdst","portdst","proto","action","date","regle"])
#df = pd.read_csv("data/log_clear.txt", sep="\t", encoding="utf-8", names=["date","ipsrc", "ipdst", "proto", "portsrc","portdst","regle","action", "interface_In","interface_out"], header=0)

#  Chargement des données
df = func.get_data()
df["portdst"] = pd.to_numeric(df["portdst"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

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

# Style personnalisé pour les statistiques clés avec dégradé et animation
func.st.markdown("""
    <style>
            
        .centered-subheader {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #4bcfd1; 
            font-family: monospace;
        }
        /* Conteneur global pour les statistiques */
        .stat-section {
            display: flex;
            justify-content: space-between;
            padding: 20px;
            background: linear-gradient(45deg, #FF5733, #FF8C00); /* Dégradé coucher de soleil avec des tons de rouge et orange */
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }

        /* Style pour chaque colonne */
        .stat-box {
            text-align: center;
            flex: 1;
            padding: 20px;
            background: linear-gradient(45deg, #FF5733, #FF8C00); /* Dégradé pour les boîtes aussi */
            border-radius: 8px;
            animation: fadeIn 1s ease-out; /* Animation d'apparition */
            margin: 5px;
        }

        /* Animation pour les boîtes */
        @keyframes fadeIn {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }

        /* Style pour les titres des statistiques */
        .stat-title {
            font-size: 18px;
            color: #fff;
            font-weight: bold;
            margin-bottom: 10px;
            font-family: monospace;
        }

        /* Style pour les valeurs des statistiques */
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #fff;
        }
        
    </style>
""", unsafe_allow_html=True)

# Affichage des statistiques 
st.markdown('<div class="centered-subheader">Statistiques clés</div>', unsafe_allow_html=True)


# Conteneur pour les colonnes de statistiques
col1, col2, col3 = st.columns(3)

# Application du style sur chaque colonne
with col1:
    st.markdown('<div class="stat-box"><div class="stat-title">Total des flux</div><div class="stat-value">{}</div></div>'.format(len(df)), unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stat-box"><div class="stat-title">Flux autorisés</div><div class="stat-value">{}</div></div>'.format(len(df[df["action"] == "PERMIT"])), unsafe_allow_html=True)

with col3:
    st.markdown('<div class="stat-box"><div class="stat-title">Flux rejetés</div><div class="stat-value">{}</div></div>'.format(len(df[df["action"] == "DENY"])), unsafe_allow_html=True)


st.header("Analyse des ports")

# Top 10 des ports les plus utilisés
filtered_ports = df[(df['portdst'] < 1024) & (df['action'] == 'PERMIT')]

top_10_ports = filtered_ports['portdst'].value_counts().head(10)
# Créer un DataFrame à partir de top_10_ports
df_top_10_ports = top_10_ports.reset_index()

# Renommer les colonnes
df_top_10_ports.columns = ['portdst', 'count']

df_top_10_ports = df_top_10_ports.sort_values(by='portdst')

# change type portdst à str
df_top_10_ports['portdst'] = df_top_10_ports['portdst'].astype(str)

# Ajouter le suffixe port devant chaque valeur de portdst 
df_top_10_ports['portdst'] = df_top_10_ports['portdst'].apply(lambda x: 'port '+ x)

# Sort le df 
df_top_10_ports = df_top_10_ports.sort_values(by='count', ascending=True)

st.subheader("Top 10 des ports inférieurs à 1024 avec un accès permit")
fig_10 = px.bar(df_top_10_ports,
                x='count', 
                y=df_top_10_ports['portdst'], 
                orientation='h',
                labels={'y': 'Port', 'count': 'Nombre de connexions'},
                text='count'
)
st.plotly_chart(fig_10)

# # Créer un diagramme de Sankey entre les protocoles et les actions
# st.subheader("Flux de données entre les règles et les actions")

# # Comptage des flux entre les protocoles et les actions
# df_sankey = df.groupby(['regle', 'action']).size().reset_index(name='count')

# # Créer un dictionnaire pour les noeuds (regle et actions)
# nodes = pd.concat([df_sankey['regle'], df_sankey['action']]).unique()
# node_dict = {node: i for i, node in enumerate(nodes)}

# # Créer les liens pour le Sankey
# links = df_sankey.apply(lambda row: {
#     "source": node_dict[row['regle']],
#     "target": node_dict[row['action']],
#     "value": row['count']
# }, axis=1).tolist()

# # Préparer la figure Sankey
# fig_sankey = go.Figure(go.Sankey(
#     node=dict(
#         pad=15,  # Espace autour des noeuds
#         thickness=20,  # Largeur des noeuds
#         line=dict(color="black", width=0.5),  # Bordure des noeuds
#         label=nodes  # Labels des noeuds
#     ),
#     link=dict(
#         source=[link["source"] for link in links],
#         target=[link["target"] for link in links],
#         value=[link["value"] for link in links],
#         color="blue"  # Couleur des liens
#     )
# ))

# # Affichage du graphique dans Streamlit
# st.plotly_chart(fig_sankey)

st.subheader("Top 5 des IPs sources les plus actives")

top_5_ips = df['ipsrc'].value_counts().head(5)
fig_top5 = px.bar(top_5_ips, 
                  x=top_5_ips.index, 
                  y=top_5_ips.values, 
                  labels={'x': 'IP Source', 'y': 'Nombre de connexions'},
                  text=top_5_ips.values
)
st.plotly_chart(fig_top5)

st.subheader("Pourcentage d'actions Deny pour les 5 IPs source les plus actives")

# Comptage des actions par IP source
df_counts = df.groupby(["ipsrc", "action"]).size().reset_index(name="count")

# Sélection des 5 IPs sources les plus actives
top_5_ips = df["ipsrc"].value_counts().head(5).index

df_top5 = df_counts[df_counts["ipsrc"].isin(top_5_ips)]


# calculer le pourcentage de deny par ip source
df_top5 = df_top5.reset_index(drop=True)
df_top5['percent'] = df_top5.groupby('ipsrc')['count'].apply(lambda x: x / x.sum() * 100).values

# Sort par ip filtrer pour uniquement que les deny
df_top5 = df_top5[df_top5['action'] == 'DENY']
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

# Drop les lignes avec des nan
df.dropna(subset=['ipsrc', 'ipdst'], inplace=True)

university_ip_ranges = [
    #ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('159.84.0.0/16'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('10.0.0.0/8'),
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

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Fonction pour vérifier si une IP est hors des plages définies
def is_outside_university(ip):
    return not any(ipaddress.ip_address(ip) in net for net in university_ip_ranges)

# df["is_outside"] = df["ipsrc"].apply(lambda ip: not any(ipaddress.ip_address(ip) in ipaddress.ip_network(net) for net in university_ip_ranges))

# st.dataframe(df)

# Filtrer les lignes où soit `ipsrc` soit `ipdst` est hors des plages
# df_valid = df[df["ipsrc"].apply(is_valid_ip) & df["ipdst"].apply(is_valid_ip)]
# filtered_df = df_valid[df_valid["ipsrc"].apply(is_outside_university) | df_valid["ipdst"].apply(is_outside_university)]

# df_valid = df[df["ipsrc"].apply(is_valid_ip) & df["ipdst"].apply(is_valid_ip)]

# # Filtrer les adresses IP invalides
# df = df[df['ipsrc'].apply(is_valid_ip)]

# Lister les accès des adresses non incluses dans le plan d'adressage de l'Université
st.subheader("Accès des adresses non incluses dans le plan d'adressage de l'Université")

non_university_accesses = df[~df['ipsrc'].apply(is_university_ip)]

# Adress unique des IP sources non incluses

col4, col5 = st.columns(2)
with col4:
    st.markdown('<div class="stat-box"><div class="stat-title">Nombre d\'adresses IP sources non incluses</div><div class="stat-value">{}</div></div>'.format(non_university_accesses['ipsrc'].shape[0]), unsafe_allow_html=True)

with col5 : 
    st.markdown('<div class="stat-box"><div class="stat-title">Nombre d\'adresses IP sources uniques non incluses</div><div class="stat-value">{}</div></div>'.format(non_university_accesses['ipsrc'].nunique()), unsafe_allow_html=True)


st.write(non_university_accesses)

# piechart pour les actions pour les adresses non incluses dans le plan d'adressage de l'Université
fig_pie = px.pie(non_university_accesses, names='action', title='Répartition des actions pour les adresses non incluses')
st.plotly_chart(fig_pie)

st.subheader("Analyse des IP sources et destinations")

# Calculer le nombre total de connexions par IP source, action et IP destination
df_count = df.groupby(['ipsrc', 'action', 'ipdst']).size().reset_index(name='total_connections')

# Ajouter un curseur pour filtrer les données en fonction du nombre total de connexions
min_conn, max_conn = df_count['total_connections'].min(), df_count['total_connections'].max()
selected_range = st.slider("Sélectionnez la plage de connexions totales", min_conn, max_conn, (min_conn, max_conn))

# Filtrer les données en fonction de la plage sélectionnée
filtered_df_count = df_count[(df_count['total_connections'] >= selected_range[0]) & (df_count['total_connections'] <= selected_range[1])]

fig_slider = px.scatter(filtered_df_count, x="ipsrc", y="total_connections", color="action",
                        symbol="action", 
                        symbol_map={"PERMIT": "circle", "DENY": "cross"},
                        color_discrete_map={"PERMIT": "blue", "DENY": "red"},
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
    color='action',  
    symbol='action',  
    color_discrete_map={'PERMIT': 'blue', 'DENY': 'red'},  
    symbol_map={'PERMIT': 'circle', 'DENY': 'cross'},
    title=f"Connexions vers IP destination depuis {selected_ipsrc}",
    labels={'ipdst': 'IP destination', 'Count': 'Nombre de connexions'}
)

# Affichage du graphique
st.plotly_chart(fig_scatter)



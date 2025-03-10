import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

#  Fonction pour charger les données depuis la base SQLite
@st.cache_data
def load_data():
    conn = sqlite3.connect("./data/database.db")
    query = "SELECT ipsrc, ipdst, portdst, proto, action, date, regle FROM logs_data"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

#  Chargement des données
df = load_data()

#  Interface
st.markdown("""
    <h1 style="font-size: 36px; color: #4bcfd1; text-align: center; font-family: 'Arial', sans-serif;">
        🔍 <span style="font-weight: bold;">Exploration des Flux Réseau</span> 🔍
    </h1>
    <p style="font-size: 18px; color: #a8e5e4; text-align: center; font-family: 'Arial', sans-serif;">
        Visualisation et analyse des flux autorisés et rejetés par protocole et par port.
    </p>
""", unsafe_allow_html=True)

st.write("")  # Espacement

# Style personnalisé pour les filtres
st.markdown("""
    <style>
        .filter-section {
            background: #2c3e50;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }

        /* Appliquer le style directement aux éléments de filtre */
        .stSelectbox, .stSlider {
            background: linear-gradient(45deg, #FF5733, #FF8C00); /* Dégradé coucher de soleil avec des tons de rouge et orange */
            color: #ecf0f1;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        }

        .stSelectbox label, .stSlider label {
            color: #ecf0f1;
            font-size: 16px;
        }

        /* Appliquer un espacement entre les filtres */
        .stSelectbox, .stSlider {
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Conteneur pour les filtres
with st.container():
    # Filtres dans les colonnes
    col1, col2, col3 = st.columns(3)

    with col1:
        protocole_choice = st.selectbox("Sélectionner un protocole", ["Tous"] + df["proto"].unique().tolist())

    with col2:
        flux_choice = st.selectbox("Sélectionner le type de flux", ["Tous"] + df["action"].unique().tolist())

    with col3:
        min_port, max_port = int(df["portdst"].min()), int(df["portdst"].max())
        port_range = st.slider("Plage de ports", min_port, max_port, (min_port, max_port))



#  Application des filtres
df_filtered = df.copy()
if protocole_choice != "Tous":
    df_filtered = df_filtered[df_filtered["proto"] == protocole_choice]
if flux_choice != "Tous":
    df_filtered = df_filtered[df_filtered["action"] == flux_choice]
df_filtered = df_filtered[df_filtered["portdst"].between(port_range[0], port_range[1])]

# Style personnalisé pour les statistiques clés avec dégradé et animation
st.markdown("""
    <style>
            
        .centered-subheader {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #4bcfd1; 
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
        }

        /* Style pour les valeurs des statistiques */
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #fff;
        }
    </style>
""", unsafe_allow_html=True)

# Ajouter les onglets Tableau et Graphiques
tabs = st.tabs(["Tableau", "Graphiques"])
with tabs[0]:

    # # Affichage des statistiques 
    # st.markdown('<div class="centered-subheader">Statistiques clés</div>', unsafe_allow_html=True)


    # # Conteneur pour les colonnes de statistiques
    # col1, col2, col3 = st.columns(3)

    # # Application du style sur chaque colonne
    # with col1:
    #     st.markdown('<div class="stat-box"><div class="stat-title">Total des flux</div><div class="stat-value">{}</div></div>'.format(len(df_filtered)), unsafe_allow_html=True)

    # with col2:
    #     st.markdown('<div class="stat-box"><div class="stat-title">Flux autorisés</div><div class="stat-value">{}</div></div>'.format(len(df_filtered[df_filtered["action"] == "Autorisé"])), unsafe_allow_html=True)

    # with col3:
    #     st.markdown('<div class="stat-box"><div class="stat-title">Flux rejetés</div><div class="stat-value">{}</div></div>'.format(len(df_filtered[df_filtered["action"] == "Rejeté"])), unsafe_allow_html=True)


    # Tableau style
    st.markdown("""
        <style>
        
                
        /* Appliquer le style directement aux éléments de filtre */
        .stPlotlyChart {
            background: #34495e;
            color: #ecf0f1;
            border-radius: 10px;
            padding-top : 10px;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
           
        }
        </style>
    """, unsafe_allow_html=True)

    # Affichage du tableau interactif
    st.subheader("Détails des flux")
    
    st.data_editor(df_filtered, use_container_width=True, hide_index=True)


 #Graphiques à afficher dans 4 blocs
with tabs[1]:
    # Conteneur pour les 4 graphiques
    col1, col2 = st.columns(2)

    with col1:
        # 1. Distribution des flux par protocole
        fig1 = px.histogram(df_filtered, x="proto", color="action", barmode="stack", title="Répartition des flux par protocole")
        st.plotly_chart(fig1, use_container_width=True) 


        
        # 2. Répartition des flux autorisés et rejetés par port
        fig2 = px.histogram(df_filtered, x="portdst", color="action", barmode="group", title="Répartition des flux autorisés et rejetés par port")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # 3. Flux par heure de la journée
        df_filtered['hour'] = pd.to_datetime(df_filtered['date']).dt.hour
        fig3 = px.line(df_filtered.groupby('hour').size().reset_index(name='count'), x='hour', y='count', title="Flux par heure de la journée")
        st.plotly_chart(fig3, use_container_width=True)

        # 4. Top 10 des adresses IP source les plus actives
        ip_counts = df_filtered['ipsrc'].value_counts().head(10)
        fig4 = px.bar(ip_counts, x=ip_counts.index, y=ip_counts.values, title="Top 10 des adresses IP source les plus actives", labels={'x': 'IP Source', 'y': 'Nombre de flux'})
        st.plotly_chart(fig4, use_container_width=True)

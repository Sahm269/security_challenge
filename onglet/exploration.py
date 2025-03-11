from analyses import fonctions as func
# import streamlit as st
# import sqlite3
# import pandas as pd
import plotly.express as px



#  Chargement des données
df = func.get_data()
df["portdst"] = func.pd.to_numeric(df["portdst"], errors="coerce")
df["date"] = func.pd.to_datetime(df["date"], errors="coerce")
#  Interface
func.st.markdown("""
    <h1 style="font-size: 36px; color: #4bcfd1; text-align: center; font-family: 'Arial', sans-serif;">
        🔍 <span style="font-weight: bold;">Exploration des Flux Réseau</span> 🔍
    </h1>
    <p style="font-size: 18px; color: #a8e5e4; text-align: center; font-family: 'Arial', sans-serif;">
        Visualisation et analyse des flux autorisés et rejetés par protocole et par port.
    </p>
""", unsafe_allow_html=True)

func.st.write("")  # Espacement

# Style personnalisé pour les filtres
func.st.markdown("""
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
with func.st.container():
    # Filtres dans les colonnes
    col1, col2, col3 = func.st.columns(3)

    with col1:
        protocole_choice = func.st.selectbox("Sélectionner un protocole", ["Tous"] + df["proto"].unique().tolist())

    with col2:
        flux_choice = func.st.selectbox("Sélectionner le type de flux", ["Tous"] + df["action"].unique().tolist())

    with col3:


        min_port, max_port = int(df["portdst"].min()), int(df["portdst"].max())
        port_range = func.st.slider("Plage de ports", min_port, max_port, (min_port, max_port))



#  Application des filtres
df_filtered = df.copy()
if protocole_choice != "Tous":
    df_filtered = df_filtered[df_filtered["proto"] == protocole_choice]
if flux_choice != "Tous":
    df_filtered = df_filtered[df_filtered["action"] == flux_choice]
df_filtered = df_filtered[df_filtered["portdst"].between(port_range[0], port_range[1])]

# Style personnalisé pour les statistiques clés avec dégradé et animation
func.st.markdown("""
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
tabs = func.st.tabs(["Tableau", "Graphiques"])
with tabs[0]:

    # Comptage des flux PERMIT/DENY par protocole
    flux_counts = df_filtered.groupby(["proto", "action"]).size().unstack(fill_value=0)

    # Affichage du nombre de flux rejetés par protocole
    func.st.write("### Nombre de flux par protocole et action")
    func.st.write(flux_counts)


   

    # Tableau style
    func.st.markdown("""
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
    func.st.subheader("Détails des flux")
    
    func.st.data_editor(df_filtered, use_container_width=True, hide_index=True)


    #Graphiques à afficher dans 4 blocs
    with tabs[1]:
        # Conteneur pour les 4 graphiques
        col1, col2 = func.st.columns(2)

        with col1:
            # 📊 1. Répartition des flux autorisés vs rejetés par protocole
            fig1 = px.bar(df_filtered.groupby(["proto", "action"]).size().reset_index(name="count"),
                        x="proto", y="count", color="action", barmode="group",
                        title="Répartition des flux autorisés vs rejetés par protocole")
            func.st.plotly_chart(fig1, use_container_width=True)

            # 📈 2. Évolution temporelle des flux (par protocole et action)
            df_time = df_filtered.groupby([func.pd.Grouper(key="date", freq="D"), "action"]).size().reset_index(name="count")
            fig2 = px.line(df_time, x="date", y="count", color="action",
                        title="Évolution temporelle des flux")
            func.st.plotly_chart(fig2, use_container_width=True)

        with col2:
            # 📊 3. Distribution des ports de destination utilisés
            fig3 = px.histogram(df_filtered, x="portdst", nbins=30, color="proto",
                                title="Distribution des ports de destination utilisés")
            func.st.plotly_chart(fig3, use_container_width=True)

            # 🥧 4. Répartition des flux par règles du firewall
            fig4 = px.pie(df_filtered, names="regle", title="Répartition des flux par règles du firewall")
            func.st.plotly_chart(fig4, use_container_width=True)

import streamlit as st

# Titre principal
st.markdown("""
    <h1 style="font-size: 36px; color: #4bcfd1; text-align: center; font-family: 'Arial', sans-serif;">
        📄 <span style="font-weight: bold;">À propos de l'application</span> 📄
    </h1>
    <p style="font-size: 18px; color: #a8e5e4; text-align: center; font-family: 'Arial', sans-serif;">
        Découvrez les objectifs, les technologies et les créateurs derrière cette application !
    </p>
""", unsafe_allow_html=True)

st.write("")  # Espacement

# CSS pour uniformiser la hauteur des blocs
st.markdown("""
    <style>
        .custom-block {
            background: #1a1e32;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            height: 300px; /* Hauteur fixe pour uniformiser */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin-top:20px;
            
        }

        .custom-block h2 {
            color: #4bcfd1;
            font-size: 22px;
            text-align: center;
            font-family: monospace;
        }
        .custom-block p, .custom-block ul {
            font-size: 16px;
            color: #a8e5e4;
            font-family: monospace;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# Disposition en deux lignes et deux colonnes
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Bloc 1 : Utilisation de l'application
with col1:
    st.markdown("""
        <div class="custom-block" style="background: #151927;">
            <h2>🖥️ Utilisation de l'application 🖥️</h2>
            <p>Cette application a pour but de comparer et d'analyser les commentaires TripAdvisor.</p>
            <p>Vous trouverez quatre onglets :</p>
            <ul>
                <li><strong>🏠 Accueil :</strong> Informations générales</li>
                <li><strong>📊 Dashboard :</strong> Comparer les restaurants</li>
                <li><strong>🔍 Exploration :</strong> Analyse détaillée</li>
                <li><strong>⚠️ Détection d'anomalies :</strong> Ajouter un restaurant</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Bloc 2 : Technologies utilisées
with col2:
    st.markdown("""
        <div class="custom-block" style="background: #161A2C;">
            <h2>🤖 Technologies utilisées 🤖</h2>
            <p>Cette application a été développée avec :</p>
            <ul>
                <li>Python</li>
                <li>Streamlit (interface utilisateur)</li>
                <li>Pandas (manipulation des données)</li>
                <li>Plotly (visualisations graphiques)</li>
                <li>SQLite (base de données)</li>
               
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Bloc 3 : Fonctionnalités
with col3:
    st.markdown("""
        <div class="custom-block" style="background: #161A2C;">
            <h2>⚙️ Fonctionnalités ⚙️</h2>
            <p>Notre application offre les fonctionnalités suivantes :</p>
            <ul>
                <li> Analyse descriptive des flux rejetés et autorisés par protocoles (TCP, UDP) </li>
                <li> Visualisation interactive des données</li>
                <li> Un Dashboard intuitif avec des statistiques clés</li>
                <li> Et une partie machine learning </li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Bloc 4 : Créateurs
with col4:
    st.markdown("""
        <div class="custom-block" style="background: #151927;">
            <h2>👥 Créateurs 👥</h2>
            <p>Cette application a été développée par <strong>Bértrand Klein</strong>, 
            <strong>Souraya Ahmed Abderemane</strong>, et <strong>Lucile Perbet</strong>, dans le cadre 
            du cours de Sécurité du master SISE de l'Université Lumière Lyon 2.</p>
        </div>
    """, unsafe_allow_html=True)
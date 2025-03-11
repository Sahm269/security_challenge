import streamlit as st
import base64

st.set_page_config(page_title=" security", page_icon="assets/logo.png", layout="wide")


def add_logo():

    # Lecture du fichier image local
    with open("assets/logo.png", "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url("data:image/png;base64,{logo_data}");
                background-repeat: no-repeat;
                padding-top: 275px;
                background-position: center -50px;
                background-size: 100%;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


add_logo()
# Définition des onglets
accueil = st.Page("onglet/accueil.py", title=" 🏠 Accueil")
dashboard = st.Page("onglet/dashboard.py", title="📊 Dashboard")
exploration = st.Page("onglet/exploration.py", title="🔍 Exploration")
detection = st.Page("onglet/detection.py", title="⚠️ Détection d'anomalies")

pg = st.navigation([accueil,dashboard,exploration,detection])
pg.run()
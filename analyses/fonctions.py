import sqlite3
import pandas as pd

import streamlit as st

@st.cache_data
def load_data():
    """Charge les données depuis la base SQLite et les retourne sous forme de DataFrame."""
    conn = sqlite3.connect("./data/database1.db")
    query = "SELECT ipsrc, ipdst, portdst, proto, action, date, regle FROM logs_data"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_data():
    """Vérifie si les données sont déjà chargées, sinon les charge une seule fois."""
    if "df" not in st.session_state:
        st.session_state.df = load_data()
    return st.session_state.df

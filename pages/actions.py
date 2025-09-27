import streamlit as st
import pandas as pd
from database import SessionLocal
from crud import get_historique_ac

st.set_page_config(page_title="Historique des actions", page_icon="📘", layout="wide")

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.switch_page("app.py")

if st.session_state.get("role") != "admin":
    st.switch_page("pages/home.py")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())

st.title(f"Historique des actions ({st.session_state['role']})")

actions = get_historique_ac(db)

if actions:
    data = [
        {
            "ID Utilisateur": a.utilisateur_id,
            "Nom": a.nom,
            "Rôle": a.role,
            "Action": a.action,
            "Cible": a.cible,
            "Détails": a.details,
            "Date": a.date_action.strftime("%Y-%m-%d %H:%M:%S")
        }
        for a in actions
    ]
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aucune action enregistrée pour le moment.")







role = st.session_state.get("role", "user")

col = st.sidebar.container()

if col.button("Accueil", use_container_width=True):
    st.switch_page("pages/home.py")

if role == "admin":
    if col.button("Utilisateurs", use_container_width=True):
        st.switch_page("pages/users.py")
    if col.button("Historique Connexions", use_container_width=True):
        st.switch_page("pages/historique.py")
    if col.button("Historique Actions", use_container_width=True):
        st.switch_page("pages/actions.py")

if col.button("Déconnexion", use_container_width=True):
    st.session_state.clear()
    st.rerun()


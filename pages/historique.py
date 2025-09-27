import streamlit as st
import pandas as pd
from database import SessionLocal
from crud import get_historique

st.set_page_config(page_title="Historique", page_icon="📜", layout="wide")


if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("Vous devez vous connecter d'abord!")
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

st.title(f"Session {st.session_state['role']}")


historique = get_historique(db)

st.write("Liste de connextion des utilisateurs")
if historique:
    data = [
        {
            "ID": h.utilisateur_id,
            "Nom": h.nom,
            "Role": h.role,
            "Date": h.date_connexion.strftime("%Y-%m-%d %H:%M:%S")
        }
        for h in historique
    ]
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)








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







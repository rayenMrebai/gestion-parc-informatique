import streamlit as st
from database import SessionLocal
from crud import add_historique
from crud import authenticate_user

st.set_page_config(page_title="User Login", layout="wide")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())


def login_page():
    st.title("Connexion")
    st.write("Entrez vos identifiants pour vous connecter.")

    with st.form("login_form"):
        nom = st.text_input("Nom")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")

    if submit:
        if not nom or not password:
            st.error("Veuillez remplir tous les champs.")
        else:
            user = authenticate_user(db, nom, password)
            if user:
                add_historique(db, user.id, user.nom, user.role)
                st.success("Connexion réussie !")
                st.session_state["authenticated"] = True
                st.session_state["id"] = user.id
                st.session_state["nom"] = user.nom
                st.session_state["role"] = user.role
                st.session_state["password"] = user.password
                st.rerun()
            else:
                st.error("Nom ou mot de passe incorrect.")


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_page()
else:
    st.switch_page("pages/home.py")  
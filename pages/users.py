import streamlit as st
import pandas as pd
from database import SessionLocal
from crud import get_users, add_user, update_user, delete_user, check_name_exists, change_role
from crud import add_historique_ac


st.set_page_config(page_title="Utilisateurs", page_icon="👤", layout="wide")

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("Vous devez vous connecter d'abord!")
    st.rerun()

if st.session_state.get("role") != "admin":
    st.warning("Accès réservé aux admins.")
    st.stop()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())

def action(db, action, cible, details=""):
    add_historique_ac(
        db=db,
        utilisateur_id=st.session_state.get("id"),
        nom=st.session_state.get("nom"),
        role=st.session_state.get("role"),
        action=action,
        cible=cible,
        details=details
    )

st.title(f"Session {st.session_state['role']}")

st.write("Liste des utilisateurs")
users = get_users(db)
if users:
    users_df = pd.DataFrame(users, columns=["ID", "Nom", "Role"])
    st.table(users_df)


col1, col2, col3, col4 = st.columns(4)
if col1.button("Ajouter", use_container_width=True):
    st.session_state["show_add"] = True
if col2.button("Modifier", use_container_width=True):
    st.session_state["show_edit"] = True
if col3.button("Supprimer", use_container_width=True):
    st.session_state["show_delete"] = True
if col4.button("Changer Rôle", use_container_width=True):
    st.session_state["show_role"] = True

if st.button("Annuler l'opération", use_container_width=True):
    st.session_state["show_add"] = False
    st.session_state["show_edit"] = False
    st.session_state["show_delete"] = False
    st.session_state["show_role"] = False
    st.rerun()

if st.session_state.get("show_add"):
    st.subheader("Ajouter un utilisateur")
    with st.form("form_add"):
        name = st.text_input("Nom")
        role = st.selectbox("Rôle", ["admin", "user"])
        pwd = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Ajouter")
        if submitted:
            if not name or not role or not pwd:
                st.error("Veuillez remplir tous les champs.")
            elif check_name_exists(db, name):
                st.error("Ce nom existe déjà.")
            else:
                add_user(db, name, role, pwd)
                action(db, "ajout", "utilisateur", f"Ajout de l'utilisateur {name}")
                st.success(f"Utilisateur {name} ajouté.")
                st.session_state["show_add"] = False
                st.rerun()

if st.session_state.get("show_edit"):
    st.subheader("Modifier un utilisateur")
    with st.form("form_edit"):
        cur_nom = st.text_input("Nom de l'utilisateur à modifier")
        new_nom = st.text_input("Nouveau nom")
        new_pwd = st.text_input("Nouveau mot de passe", type="password")
        submitted = st.form_submit_button("Modifier")
        if submitted:
            if not cur_nom:
                st.error("Veuillez saisir un nom.")
            elif not check_name_exists(db, cur_nom):
                st.error("Nom inexistant.")
            else:
                if not new_nom and not new_pwd:
                    st.warning("Aucune modification détectée.")
                else:
                    if new_nom and new_nom != cur_nom and check_name_exists(db, new_nom):
                        st.error("Ce nouveau nom est déjà utilisé.")
                    else:
                        update_user(db, cur_nom, new_nom, new_pwd)
                        action(db, "modification", "utilisateur", f"Modification de l'utilisateur {cur_nom}")
                        st.success(f"Utilisateur {cur_nom} modifié.")
                        st.session_state["show_edit"] = False
                        st.rerun()

if st.session_state.get("show_delete"):
    st.subheader("Supprimer un utilisateur")
    with st.form("form_delete"):
        nom_del = st.text_input("Nom à supprimer")
        submitted = st.form_submit_button("Supprimer")
        if submitted:
            if not nom_del:
                st.error("Veuillez saisir un nom.")
            elif not check_name_exists(db, nom_del):
                st.error("Nom inexistant.")
            elif nom_del == st.session_state["nom"]:
                st.error("Vous ne pouvez pas vous supprimer.")
            else:
                delete_user(db, nom_del)
                action(db, "suppression", "utilisateur", f"Suppression de l'utilisateur {nom_del}")
                st.success(f"Utilisateur {nom_del} supprimé.")
                st.session_state["show_delete"] = False
                st.rerun()

if st.session_state.get("show_role"):
    st.subheader("Changer le rôle d'un utilisateur")
    with st.form("form_role"):
        nom_user = st.text_input("Nom de l'utilisateur")
        new_role = st.selectbox("Nouveau rôle", ["admin", "user"])
        submitted = st.form_submit_button("Changer")
        if submitted:
            if not nom_user:
                st.error("Veuillez saisir un nom.")
            elif nom_user == st.session_state["nom"]:
                st.error("Vous ne pouvez pas changer votre propre rôle.")
            elif not check_name_exists(db, nom_user):
                st.error("Nom inexistant.")
            else:
                change_role(db, nom_user, new_role)
                action(db, "modification", "utilisateur", f"Changement de rôle de {nom_user} en {new_role}")
                st.success(f"Rôle de {nom_user} modifié.")
                st.session_state["show_role"] = False
                st.rerun()




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


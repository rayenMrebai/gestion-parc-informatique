from sqlalchemy.orm import Session
from models import HistoriqueConnexion 
from datetime import datetime

def get_historique(db: Session):
    return db.query(HistoriqueConnexion).all()

def add_historique(db: Session, utilisateur_id: int, nom: str, role: str):
    historique = HistoriqueConnexion(
        utilisateur_id=utilisateur_id,
        nom=nom,
        role=role,
        date_connexion=datetime.now()
    )
    db.add(historique)
    db.commit()
    db.refresh(historique)
    return historique

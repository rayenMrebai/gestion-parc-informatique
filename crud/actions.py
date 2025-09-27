from sqlalchemy.orm import Session
from models import HistoriqueAction 
from datetime import datetime

def get_historique_ac(db: Session):
    return db.query(HistoriqueAction).all()

def add_historique_ac(db: Session,utilisateur_id: int,nom: str,role: str,action: str,cible: str,details: str = None):
        historique = HistoriqueAction(
            utilisateur_id=utilisateur_id,
            nom=nom,
            role=role,
            action=action,
            cible=cible,
            details=details,
            date_action=datetime.now()
        )
        db.add(historique)
        db.commit()
        db.refresh(historique)
        return historique
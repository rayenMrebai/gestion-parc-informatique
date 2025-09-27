from sqlalchemy.orm import Session
from models import Ligne

def fetch_lignes(db: Session, project_id: int):
    return db.query(Ligne).filter(Ligne.project_id == project_id).all()

def add_ligne(db: Session, project_id: int, name: str):
    ligne = Ligne(project_id=project_id, name=name)
    db.add(ligne)
    db.commit()
    db.refresh(ligne)
    return ligne

def update_ligne(db: Session, ligne_id: int, new_name: str):
    ligne = db.query(Ligne).filter(Ligne.id == ligne_id).first()
    if ligne:
        ligne.name = new_name
        db.commit()
        db.refresh(ligne)
    return ligne

def delete_ligne(db: Session, ligne_id: int):
    ligne = db.query(Ligne).filter(Ligne.id == ligne_id).first()
    if ligne:
        db.delete(ligne)
        db.commit()

def ligne_exists(db: Session, name: str) -> bool:
    return db.query(Ligne).filter(Ligne.name == name).first() is not None

from sqlalchemy.orm import Session
from models import Poste

def fetch_postes(db: Session, ligne_id: int):
    return db.query(Poste).filter(Poste.ligne_id == ligne_id).all()

def add_poste(db: Session, ligne_id: int, name: str):
    poste = Poste(ligne_id=ligne_id, name=name)
    db.add(poste)
    db.commit()
    db.refresh(poste)
    return poste

def update_poste(db: Session, poste_id: int, new_name: str):
    poste = db.query(Poste).filter(Poste.id == poste_id).first()
    if poste:
        poste.name = new_name
        db.commit()
        db.refresh(poste)
    return poste

def delete_poste(db: Session, poste_id: int):
    poste = db.query(Poste).filter(Poste.id == poste_id).first()
    if poste:
        db.delete(poste)
        db.commit()

def poste_exists(db: Session, name: str) -> bool:
    return db.query(Poste).filter(Poste.name == name).first() is not None
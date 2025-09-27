from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Equipement, Poste, Project, Ligne

def fetch_equipements(db: Session, poste_id: int):
    return db.query(Equipement).filter(Equipement.poste_id == poste_id).all()

def add_equipement(db: Session, poste_id: int, host_name: str, equipement: str, modele: str, num_serie: str):
    equip = Equipement(
        poste_id=poste_id,
        host_name=host_name,
        equipement=equipement,
        modele=modele,
        num_serie=num_serie
    )
    db.add(equip)
    db.commit()
    db.refresh(equip)
    return equip

def update_equipement(db: Session, equipement_id: int, host_name: str, equipement: str, modele: str, num_serie: str):
    equip = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if equip:
        equip.host_name = host_name
        equip.equipement = equipement
        equip.modele = modele
        equip.num_serie = num_serie
        db.commit()
        db.refresh(equip)
    return equip

def delete_equipement(db: Session, equipement_id: int):
    equip = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if equip:
        db.delete(equip)
        db.commit()
        return True
    return False

def deplacer_equipement(db: Session, equipement_id: int, nouveau_poste_id: int):
    poste = db.query(Poste).filter(Poste.id == nouveau_poste_id).first()
    if not poste:
        return "le poste n'existe pas"
    equip = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if not equip:
        return "l'équipement n'existe pas"
    equip.poste_id = nouveau_poste_id
    db.commit()
    db.refresh(equip)
    return "Équipement déplacé avec succès"

def equipement_existe(db: Session, num_serie: str) -> bool:
    return db.query(Equipement).filter(Equipement.num_serie == num_serie).first() is not None

def get_id_by_num_serie(db: Session, num_serie: str):
    equip = db.query(Equipement).filter(Equipement.num_serie == num_serie).first()
    return equip.id if equip else None

def get_emplacement(db: Session, num_serie: str):
    result = (
        db.query(Project.name.label("projet"),Ligne.name.label("ligne"),Poste.name.label("poste")).join(Ligne, Project.lignes).join(Poste, Ligne.postes).join(Equipement, Poste.equipements).filter(Equipement.num_serie == num_serie).first()
    )
    return result

def get_equipements(db: Session, mot: str):
    like_pattern = f"%{mot}%"
    results = (
        db.query(
            Equipement.host_name.label("host_name"),
            Equipement.modele,
            Equipement.equipement,
            Equipement.num_serie,
            Project.name.label("projet"),
            Ligne.name.label("ligne"),
            Poste.name.label("poste")
        )
        .join(Poste, Equipement.poste)
        .join(Ligne, Poste.ligne)
        .join(Project, Ligne.project)
        .filter(
            or_(
                Equipement.host_name.ilike(like_pattern),
                Equipement.modele.ilike(like_pattern),
                Equipement.equipement.ilike(like_pattern),
                Equipement.num_serie.ilike(like_pattern)
            )
        )
        .order_by(Equipement.host_name)
        .all()
    )
    result_list = []
    for e in results:
        e_dict = e._asdict() if hasattr(e, '_asdict') else e.__dict__
        result_list.append(e_dict)
    return result_list

def liste_equipements(db: Session, poste_id: int):
    results = (
        db.query(
            Equipement.host_name.label("host_name"),
            Equipement.modele,
            Equipement.equipement,
            Equipement.num_serie,
            Project.name.label("projet"),
            Ligne.name.label("ligne"),
            Poste.name.label("poste")
        )
        .join(Poste, Equipement.poste)
        .join(Ligne, Poste.ligne)
        .join(Project, Ligne.project)
        .filter(Equipement.poste_id == poste_id)
        .all()
    )
    return [row._asdict() for row in results]


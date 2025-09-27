from database import SessionLocal
from models import Equipement, Poste, Ligne, Project

def delete_all_data_separately(db):
    db.query(Equipement).delete()
    db.commit()

    db.query(Poste).delete()
    db.commit()

    db.query(Ligne).delete()
    db.commit()

    db.query(Project).delete()
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        delete_all_data_separately(db)
        print("Suppression terminée.")
    except Exception as e:
        print("Erreur:", e)
    finally:
        db.close()
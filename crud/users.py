from sqlalchemy.orm import Session
from models import User
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(db: Session, nom: str, password: str):
    user = db.query(User).filter(User.nom == nom).first()
    if user and hash_password(password) == user.password:
        return user
    return None

def get_users(db: Session):
    return db.query(User.id, User.nom, User.role).all()

def check_name_exists(db: Session, nom: str) -> bool:
    return db.query(User).filter(User.nom == nom).first() is not None

def add_user(db: Session, nom: str, role: str, pwd: str):
    hashed = hash_password(pwd)
    user = User(nom=nom, role=role, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, cur_nom: str, new_nom: str = None, new_pwd: str = None):
    user = db.query(User).filter(User.nom == cur_nom).first()
    if not user:
        return None
    if new_nom:
        user.nom = new_nom
    if new_pwd:
        user.password = hash_password(new_pwd)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, nom: str):
    user = db.query(User).filter(User.nom == nom).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

def change_role(db: Session, nom: str, role: str):
    user = db.query(User).filter(User.nom == nom).first()
    if not user:
        return False
    user.role = role
    db.commit()
    db.refresh(user)
    return True
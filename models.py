from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), unique=True, nullable=False)
    role = Column(Enum('admin', 'user'), nullable=False, default='user')
    password = Column(String(255), nullable=False)

    connexions = relationship("HistoriqueConnexion", back_populates="utilisateur")
    actions = relationship("HistoriqueAction", back_populates="utilisateur")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    lignes = relationship("Ligne", back_populates="project")


class Ligne(Base):
    __tablename__ = 'lignes'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    name = Column(String(255), unique=True, nullable=False)

    project = relationship("Project", back_populates="lignes")
    postes = relationship("Poste", back_populates="ligne")


class Poste(Base):
    __tablename__ = 'postes'
    id = Column(Integer, primary_key=True)
    ligne_id = Column(Integer, ForeignKey('lignes.id', ondelete='CASCADE'))
    name = Column(String(255), unique=True, nullable=False)

    ligne = relationship("Ligne", back_populates="postes")
    equipements = relationship("Equipement", back_populates="poste")


class Equipement(Base):
    __tablename__ = 'equipements'
    id = Column(Integer, primary_key=True)
    poste_id = Column(Integer, ForeignKey('postes.id', ondelete='CASCADE'))
    host_name = Column(String(255))
    equipement = Column(String(255), nullable=False)
    modele = Column(String(255), nullable=False)
    num_serie = Column(String(255), unique=True, nullable=False)

    poste = relationship("Poste", back_populates="equipements")


class HistoriqueConnexion(Base):
    __tablename__ = 'historique_connexions'
    id = Column(Integer, primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    nom = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    date_connexion = Column(DateTime, default=datetime.utcnow)

    utilisateur = relationship("User", back_populates="connexions")

class HistoriqueAction(Base):
    __tablename__ = 'historique_actions'
    id = Column(Integer, primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    nom = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)  
    cible = Column(String(50), nullable=False)   
    details = Column(String(255))                
    date_action = Column(DateTime, default=datetime.utcnow)

    utilisateur = relationship("User", back_populates="actions")


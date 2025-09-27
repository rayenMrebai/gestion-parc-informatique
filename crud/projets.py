from sqlalchemy.orm import Session
from models import Project

def fetch_projects(db: Session):
    return db.query(Project).all()

def add_project(db: Session, name: str):
    project = Project(name=name)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def update_project(db: Session, project_id: int, new_name: str):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        project.name = new_name
        db.commit()
        db.refresh(project)
    return project

def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
    return project

def project_exists(db: Session, name: str) -> bool:
    return db.query(Project).filter(Project.name == name).first() is not None




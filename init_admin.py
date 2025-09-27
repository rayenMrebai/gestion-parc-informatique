from database import SessionLocal, init_db
from models import User
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin():
    session = SessionLocal()
    admin_user = User(
        nom='admin',
        role='admin',
        password=hash_password('admin')
    )
    session.add(admin_user)
    session.commit()
    session.close()

if __name__ == "__main__":
    create_admin()

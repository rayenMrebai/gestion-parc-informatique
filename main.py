from database import init_db, SessionLocal
from models import User

def test():
    init_db()
    print("Tables créées")

    session = SessionLocal()
    users = session.query(User).all()
    print(f"Nombre d’utilisateurs dans la base : {len(users)}")
    session.close()
    

if __name__ == "__main__":
    test()

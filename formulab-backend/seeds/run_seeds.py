import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app.models.user import User
from app.utils.security import hash_password
from seeds.seed_badges import seed_badges
from seeds.seed_exercises import seed_exercises

TEACHER_EMAIL = "mtanidab@gmail.com"
TEACHER_NAME = "Mitsuo Tanida"
TEACHER_PASSWORD = "FormuLab2026!"


def run():
    db = SessionLocal()
    try:
        teacher = db.query(User).filter(User.email == TEACHER_EMAIL).first()
        if not teacher:
            teacher = User(
                email=TEACHER_EMAIL,
                name=TEACHER_NAME,
                password_hash=hash_password(TEACHER_PASSWORD),
                role="teacher",
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            print(f"✓ Profesor creado: {TEACHER_EMAIL} / {TEACHER_PASSWORD}")
        else:
            print(f"✓ Profesor ya existe: {TEACHER_EMAIL}")

        seed_badges(db)
        seed_exercises(db, teacher.id)
        print("\n✅ Seed completado exitosamente")
        print(f"\nCredenciales de acceso:")
        print(f"  Email: {TEACHER_EMAIL}")
        print(f"  Password: {TEACHER_PASSWORD}")
        print(f"  Rol: teacher (profesor)")
    finally:
        db.close()


if __name__ == "__main__":
    run()

import csv
import io
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.submission import Submission
from app.models.ra_tracking import RATracking
from app.services.gamification_service import get_level_name


def export_students_csv(db: Session) -> bytes:
    students = db.query(User).filter(User.role == "student").all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Nombre", "Email", "XP", "Nivel", "Nombre_Nivel", "Racha",
        "Ejercicios_intentados", "Ejercicios_completados(>=70)",
        "Puntaje_promedio", "RA1_%", "RA2_%", "RA3_%", "RA4_%", "RA5_%", "Ultimo_acceso",
    ])
    for s in students:
        subs = db.query(Submission).filter(Submission.user_id == s.id, Submission.evaluation_status == "complete").all()
        attempted = len(subs)
        completed = sum(1 for sub in subs if (sub.score or 0) >= 70)
        avg_score = (sum(sub.score or 0 for sub in subs) / attempted) if attempted else 0

        trackings = {t.ra_id: t for t in db.query(RATracking).filter(RATracking.user_id == s.id).all()}
        ra_rates = []
        for ra_id in range(1, 6):
            t = trackings.get(ra_id)
            rate = (t.successes / t.attempts * 100) if (t and t.attempts > 0) else 0
            ra_rates.append(round(rate, 1))

        writer.writerow([
            s.name, s.email, s.xp, s.level, get_level_name(s.level), s.streak,
            attempted, completed, round(avg_score, 1),
            *ra_rates,
            s.last_active_date.isoformat() if s.last_active_date else "",
        ])
    return output.getvalue().encode("utf-8-sig")


def export_ra_report_csv(db: Session) -> bytes:
    from app.schemas.ra_tracking import RA_LABELS
    students = db.query(User).filter(User.role == "student").all()
    output = io.StringIO()
    writer = csv.writer(output)
    header = ["Nombre", "Email"]
    for ra_id in range(1, 6):
        header += [f"RA{ra_id}_intentos", f"RA{ra_id}_logros", f"RA{ra_id}_%"]
    writer.writerow(header)
    for s in students:
        row = [s.name, s.email]
        trackings = {t.ra_id: t for t in db.query(RATracking).filter(RATracking.user_id == s.id).all()}
        for ra_id in range(1, 6):
            t = trackings.get(ra_id)
            attempts = t.attempts if t else 0
            successes = t.successes if t else 0
            rate = round(successes / attempts * 100, 1) if attempts > 0 else 0
            row += [attempts, successes, rate]
        writer.writerow(row)
    return output.getvalue().encode("utf-8-sig")

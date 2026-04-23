from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import io
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.middleware.auth_middleware import require_teacher
from app.models.user import User
from app.models.submission import Submission
from app.models.exercise import Exercise
from app.services.export_service import export_students_csv, export_ra_report_csv

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/analytics")
def get_analytics(_: User = Depends(require_teacher), db: Session = Depends(get_db)):
    total_students = db.query(User).filter(User.role == "student").count()
    total_submissions = db.query(Submission).filter(Submission.evaluation_status == "complete").count()
    avg_score = db.query(func.avg(Submission.score)).filter(Submission.evaluation_status == "complete", Submission.score != None).scalar()
    total_exercises = db.query(Exercise).filter(Exercise.is_active == True).count()
    ai_exercises = db.query(Exercise).filter(Exercise.is_active == True, Exercise.ai_generated == True).count()

    by_type = db.query(Exercise.type, func.count(Exercise.id)).filter(Exercise.is_active == True).group_by(Exercise.type).all()
    by_difficulty = db.query(Exercise.difficulty, func.count(Exercise.id)).filter(Exercise.is_active == True).group_by(Exercise.difficulty).all()

    return {
        "total_students": total_students,
        "total_submissions": total_submissions,
        "avg_score": round(float(avg_score), 1) if avg_score else 0,
        "total_exercises": total_exercises,
        "ai_exercises": ai_exercises,
        "exercises_by_type": {t: c for t, c in by_type},
        "exercises_by_difficulty": {d: c for d, c in by_difficulty},
    }


@router.get("/export/students")
def export_students(_: User = Depends(require_teacher), db: Session = Depends(get_db)):
    content = export_students_csv(db)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=formulab_estudiantes.csv"},
    )


@router.get("/export/ra-report")
def export_ra(_: User = Depends(require_teacher), db: Session = Depends(get_db)):
    content = export_ra_report_csv(db)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=formulab_ra_report.csv"},
    )

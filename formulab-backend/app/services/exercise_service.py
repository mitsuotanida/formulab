import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.exercise import Exercise
from app.models.submission import Submission


def get_exercises(
    db: Session,
    user_id: uuid.UUID,
    exercise_type: str | None = None,
    difficulty: str | None = None,
    domain: str | None = None,
    ra_id: int | None = None,
    page: int = 1,
    per_page: int = 12,
) -> tuple[list, int]:
    query = db.query(Exercise).filter(Exercise.is_active == True)
    if exercise_type:
        query = query.filter(Exercise.type == exercise_type)
    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)
    if domain:
        query = query.filter(Exercise.domain == domain)
    if ra_id:
        query = query.filter(Exercise.ra_ids.any(ra_id))

    total = query.count()
    exercises = query.offset((page - 1) * per_page).limit(per_page).all()

    result = []
    for ex in exercises:
        user_subs = db.query(Submission).filter(
            Submission.user_id == user_id,
            Submission.exercise_id == ex.id,
            Submission.evaluation_status == "complete",
        ).all()
        best_score = max((s.score or 0 for s in user_subs), default=None) if user_subs else None
        result.append({
            "exercise": ex,
            "user_best_score": best_score,
            "user_attempts": len(user_subs),
            "hints_count": len(ex.hints) if ex.hints else 0,
        })

    return result, total


def get_exercise_by_id(db: Session, exercise_id: uuid.UUID, user_id: uuid.UUID) -> dict | None:
    ex = db.query(Exercise).filter(Exercise.id == exercise_id, Exercise.is_active == True).first()
    if not ex:
        return None
    user_subs = db.query(Submission).filter(
        Submission.user_id == user_id,
        Submission.exercise_id == ex.id,
        Submission.evaluation_status == "complete",
    ).all()
    best_score = max((s.score or 0 for s in user_subs), default=None) if user_subs else None
    return {
        "exercise": ex,
        "user_best_score": best_score,
        "user_attempts": len(user_subs),
        "hints_count": len(ex.hints) if ex.hints else 0,
    }


def create_exercise(db: Session, data: dict, created_by: uuid.UUID | None = None) -> Exercise:
    ex = Exercise(
        title=data["title"],
        description=data["description"],
        data_table=data.get("data_table"),
        domain=data["domain"],
        type=data["type"],
        difficulty=data["difficulty"],
        ra_ids=data.get("ra_ids", []),
        hints=data.get("hints", []),
        reference_solution=data.get("reference_solution"),
        ai_generated=data.get("ai_generated", False),
        generation_params=data.get("generation_params"),
        created_by=created_by,
    )
    db.add(ex)
    db.commit()
    db.refresh(ex)
    return ex


def get_hint(db: Session, exercise_id: uuid.UUID, order: int) -> dict | None:
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex or not ex.hints:
        return None
    hints = sorted(ex.hints, key=lambda h: h.get("order", 0))
    matching = [h for h in hints if h.get("order") == order]
    return matching[0] if matching else None

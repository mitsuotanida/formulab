import uuid
from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth_middleware import get_user, require_teacher
from app.models.user import User
from app.schemas.exercise import ExerciseOut, ExerciseDetail, ExerciseListResponse, ExerciseCreate, ExerciseGenerateRequest, ExerciseUpdate
from app.services import exercise_service, ai_service

router = APIRouter(prefix="/exercises", tags=["exercises"])


def _build_out(row: dict) -> ExerciseOut:
    ex = row["exercise"]
    return ExerciseOut(
        id=ex.id, title=ex.title, description=ex.description,
        data_table=ex.data_table, domain=ex.domain, type=ex.type,
        difficulty=ex.difficulty, ra_ids=ex.ra_ids or [], ai_generated=ex.ai_generated,
        hints_count=row["hints_count"], created_at=ex.created_at,
        user_best_score=row["user_best_score"], user_attempts=row["user_attempts"],
    )


@router.get("", response_model=ExerciseListResponse)
def list_exercises(
    type: str | None = Query(None),
    difficulty: str | None = Query(None),
    domain: str | None = Query(None),
    ra_id: int | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=50),
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    rows, total = exercise_service.get_exercises(db, user.id, type, difficulty, domain, ra_id, page, per_page)
    return ExerciseListResponse(data=[_build_out(r) for r in rows], total=total)


@router.get("/{exercise_id}", response_model=ExerciseDetail)
def get_exercise(exercise_id: uuid.UUID, user: User = Depends(get_user), db: Session = Depends(get_db)):
    row = exercise_service.get_exercise_by_id(db, exercise_id, user.id)
    if not row:
        raise HTTPException(404, "Ejercicio no encontrado")
    ex = row["exercise"]
    return ExerciseDetail(
        id=ex.id, title=ex.title, description=ex.description,
        data_table=ex.data_table, domain=ex.domain, type=ex.type,
        difficulty=ex.difficulty, ra_ids=ex.ra_ids or [], ai_generated=ex.ai_generated,
        hints_count=row["hints_count"], created_at=ex.created_at,
        user_best_score=row["user_best_score"], user_attempts=row["user_attempts"],
        hints=ex.hints or [],
    )


@router.get("/{exercise_id}/hints")
def get_hint(exercise_id: uuid.UUID, order: int = Query(1, ge=1), user: User = Depends(get_user), db: Session = Depends(get_db)):
    hint = exercise_service.get_hint(db, exercise_id, order)
    if not hint:
        raise HTTPException(404, "Pista no encontrada")
    return {"order": order, "text": hint.get("text", "")}


@router.post("", response_model=ExerciseOut, status_code=201)
def create_exercise(body: ExerciseCreate, teacher: User = Depends(require_teacher), db: Session = Depends(get_db)):
    ex = exercise_service.create_exercise(db, {
        "title": body.title, "description": body.description,
        "data_table": body.data_table.model_dump() if body.data_table else None,
        "domain": body.domain, "type": body.type, "difficulty": body.difficulty,
        "ra_ids": body.ra_ids, "hints": body.hints,
        "reference_solution": body.reference_solution,
    }, created_by=teacher.id)
    row = {"exercise": ex, "hints_count": len(ex.hints or []), "user_best_score": None, "user_attempts": 0}
    return _build_out(row)


@router.post("/generate", response_model=ExerciseOut, status_code=201)
def generate_exercise(body: ExerciseGenerateRequest, teacher: User = Depends(require_teacher), db: Session = Depends(get_db)):
    try:
        data = ai_service.generate_exercise(
            exercise_type=body.type,
            domain=body.domain,
            difficulty=body.difficulty,
            ra_focus=body.ra_focus,
            custom_context=body.custom_context,
        )
    except Exception as e:
        raise HTTPException(500, f"Error al generar ejercicio con IA: {str(e)}")

    data_table_dict = None
    if data.get("data_table"):
        data_table_dict = data["data_table"]

    ex = exercise_service.create_exercise(db, {
        "title": data["title"],
        "description": data["description"],
        "data_table": data_table_dict,
        "domain": body.domain,
        "type": body.type,
        "difficulty": body.difficulty,
        "ra_ids": data.get("ra_ids", body.ra_focus),
        "hints": [],
        "reference_solution": data.get("reference_solution"),
        "ai_generated": True,
        "generation_params": {"type": body.type, "domain": body.domain, "difficulty": body.difficulty, "ra_focus": body.ra_focus},
    }, created_by=teacher.id)
    row = {"exercise": ex, "hints_count": 0, "user_best_score": None, "user_attempts": 0}
    return _build_out(row)


@router.put("/{exercise_id}", response_model=ExerciseOut)
def update_exercise(exercise_id: uuid.UUID, body: ExerciseUpdate, teacher: User = Depends(require_teacher), db: Session = Depends(get_db)):
    from app.models.exercise import Exercise
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(404, "Ejercicio no encontrado")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(ex, field, value)
    db.commit()
    db.refresh(ex)
    row = {"exercise": ex, "hints_count": len(ex.hints or []), "user_best_score": None, "user_attempts": 0}
    return _build_out(row)


@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(exercise_id: uuid.UUID, teacher: User = Depends(require_teacher), db: Session = Depends(get_db)):
    from app.models.exercise import Exercise
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(404, "Ejercicio no encontrado")
    ex.is_active = False
    db.commit()

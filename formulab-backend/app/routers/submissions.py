import uuid
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.middleware.auth_middleware import get_user, require_teacher
from app.models.user import User
from app.models.submission import Submission
from app.models.exercise import Exercise
from app.schemas.submission import SubmissionCreate, SubmissionOut, SubmissionPending, SubmissionFeedback, FeedbackComponent, BadgeEarned

router = APIRouter(prefix="/submissions", tags=["submissions"])


def _evaluate_in_background(submission_id: uuid.UUID) -> None:
    db = SessionLocal()
    try:
        sub = db.query(Submission).filter(Submission.id == submission_id).first()
        if not sub:
            return
        ex = db.query(Exercise).filter(Exercise.id == sub.exercise_id).first()
        user = db.query(User).filter(User.id == sub.user_id).first()
        if not ex or not user:
            return

        from app.services import ai_service
        feedback_data = ai_service.evaluate_formulation(
            exercise_description=ex.description,
            data_table=ex.data_table,
            reference_solution=ex.reference_solution or {},
            student_submission=sub.content,
        )

        score = feedback_data.get("score", 0)
        sub.score = score
        sub.feedback = feedback_data
        sub.evaluation_status = "complete"

        from app.services.gamification_service import update_streak, calculate_xp, apply_xp_and_level, check_badges
        update_streak(user, date.today())

        is_first = db.query(Submission).filter(
            Submission.user_id == user.id,
            Submission.evaluation_status == "complete",
            Submission.id != submission_id,
        ).count() == 0

        xp_earned = calculate_xp(ex.difficulty, score, sub.hints_used, user.streak, is_first)
        sub.xp_earned = xp_earned

        leveled_up, new_level_name = apply_xp_and_level(user, xp_earned)

        from app.services.ra_service import update_ra_tracking
        update_ra_tracking(db, user, ex.ra_ids or [], score)

        newly_earned_badges = check_badges(db, user, sub, ex.type)
        db.commit()
    except Exception as e:
        db = SessionLocal()
        sub = db.query(Submission).filter(Submission.id == submission_id).first()
        if sub:
            sub.evaluation_status = "error"
            sub.feedback = {"overall": f"Error en evaluación: {str(e)}", "variables": {"score": 0, "max": 25, "comment": ""}, "objective": {"score": 0, "max": 25, "comment": ""}, "constraints": {"score": 0, "max": 40, "comment": ""}, "classification": {"score": 0, "max": 10, "comment": ""}, "hints": []}
            db.commit()
    finally:
        db.close()


@router.post("", status_code=202)
def submit_formulation(
    body: SubmissionCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    ex = db.query(Exercise).filter(Exercise.id == body.exercise_id, Exercise.is_active == True).first()
    if not ex:
        raise HTTPException(404, "Ejercicio no encontrado")

    MAX_ATTEMPTS_PER_DAY = 3
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    attempts_today = db.query(Submission).filter(
        Submission.user_id == user.id,
        Submission.exercise_id == body.exercise_id,
        Submission.created_at >= today_start,
    ).count()
    if attempts_today >= MAX_ATTEMPTS_PER_DAY:
        raise HTTPException(
            status_code=403,
            detail=f"Has alcanzado el límite de {MAX_ATTEMPTS_PER_DAY} intentos diarios para este ejercicio. Vuelve mañana."
        )

    sub = Submission(
        user_id=user.id,
        exercise_id=body.exercise_id,
        content=body.content,
        hints_used=body.hints_used,
        time_spent_sec=body.time_spent_sec,
        evaluation_status="pending",
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)

    background_tasks.add_task(_evaluate_in_background, sub.id)

    return SubmissionPending(
        submission_id=sub.id,
        status="evaluating",
        poll_url=f"/api/v1/submissions/{sub.id}",
    )


@router.get("/{submission_id}", response_model=SubmissionOut)
def get_submission(submission_id: uuid.UUID, user: User = Depends(get_user), db: Session = Depends(get_db)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(404, "Submission no encontrada")
    if sub.user_id != user.id and user.role != "teacher":
        raise HTTPException(403, "Sin acceso")

    feedback_obj = None
    if sub.feedback:
        f = sub.feedback
        feedback_obj = SubmissionFeedback(
            overall=f.get("overall", ""),
            variables=FeedbackComponent(**f["variables"]) if "variables" in f else FeedbackComponent(score=0, max=25, comment=""),
            objective=FeedbackComponent(**f["objective"]) if "objective" in f else FeedbackComponent(score=0, max=25, comment=""),
            constraints=FeedbackComponent(**f["constraints"]) if "constraints" in f else FeedbackComponent(score=0, max=40, comment=""),
            classification=FeedbackComponent(**f["classification"]) if "classification" in f else FeedbackComponent(score=0, max=10, comment=""),
            hints=f.get("hints", []),
        )

    return SubmissionOut(
        id=sub.id,
        exercise_id=sub.exercise_id,
        score=sub.score,
        xp_earned=sub.xp_earned,
        hints_used=sub.hints_used,
        evaluation_status=sub.evaluation_status,
        feedback=feedback_obj,
        badges_earned=[],
        created_at=sub.created_at,
    )


@router.get("/exercise/{exercise_id}", response_model=list[SubmissionOut])
def get_submissions_for_exercise(exercise_id: uuid.UUID, user: User = Depends(get_user), db: Session = Depends(get_db)):
    subs = db.query(Submission).filter(
        Submission.user_id == user.id,
        Submission.exercise_id == exercise_id,
    ).order_by(Submission.created_at.desc()).all()
    return [SubmissionOut(
        id=s.id, exercise_id=s.exercise_id, score=s.score,
        xp_earned=s.xp_earned, hints_used=s.hints_used,
        evaluation_status=s.evaluation_status, created_at=s.created_at,
    ) for s in subs]

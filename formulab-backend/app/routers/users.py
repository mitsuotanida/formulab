import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import get_db
from app.middleware.auth_middleware import get_user, require_teacher
from app.models.user import User
from app.models.submission import Submission
from app.models.badge import UserBadge, Badge
from app.schemas.user import UserOut, UserUpdate, LeaderboardResponse, LeaderboardEntry, BadgeOut, ProgressStats
from app.services.gamification_service import get_level_name
from app.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def get_me(user: User = Depends(get_user), db: Session = Depends(get_db)):
    user_badges = (
        db.query(Badge)
        .join(UserBadge, UserBadge.badge_id == Badge.id)
        .filter(UserBadge.user_id == user.id)
        .all()
    )
    result = UserOut.model_validate(user)
    result.badges = [BadgeOut(id=b.id, name=b.name, description=b.description, icon=b.icon) for b in user_badges]
    return result


@router.patch("/me", response_model=UserOut)
def update_me(body: UserUpdate, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if body.name:
        user.name = body.name
    if body.nickname is not None:
        user.nickname = body.nickname.strip() or None
    if body.password:
        user.password_hash = hash_password(body.password)
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)


@router.get("/leaderboard", response_model=LeaderboardResponse)
def leaderboard(
    period: str = Query("all_time", pattern="^(weekly|all_time)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    _: User = Depends(get_user),
):
    from datetime import datetime, timedelta

    query = db.query(
        User,
        func.count(Submission.id).filter(Submission.score >= 70).label("exercises_completed"),
    ).outerjoin(Submission, Submission.user_id == User.id)

    if period == "weekly":
        week_ago = datetime.utcnow() - timedelta(days=7)
        query = query.filter(Submission.created_at >= week_ago)

    query = query.filter(User.role == "student").group_by(User.id).order_by(desc(User.xp))

    total = query.count()
    rows = query.offset((page - 1) * per_page).limit(per_page).all()

    entries = []
    for rank, (u, completed) in enumerate(rows, start=(page - 1) * per_page + 1):
        entries.append(LeaderboardEntry(
            rank=rank, user_id=u.id, name=u.name, nickname=u.nickname, xp=u.xp, level=u.level,
            level_name=get_level_name(u.level), streak=u.streak, exercises_completed=completed or 0,
        ))

    return LeaderboardResponse(data=entries, total=total, page=page, per_page=per_page)


@router.get("/progress-stats", response_model=ProgressStats)
def progress_stats(user: User = Depends(get_user), db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == "student").all()
    xp_list = sorted(u.xp for u in students)
    n = len(xp_list)

    def pct(data: list, p: float) -> float:
        if not data:
            return 0.0
        idx = (len(data) - 1) * p / 100
        lo = int(idx)
        hi = min(lo + 1, len(data) - 1)
        return data[lo] + (data[hi] - data[lo]) * (idx - lo)

    above = sum(1 for x in xp_list if x < user.xp)
    percentile = round(above / n * 100) if n > 0 else 0

    return ProgressStats(
        user_xp=user.xp,
        user_percentile=percentile,
        count=n,
        min=float(xp_list[0]) if xp_list else 0.0,
        q1=pct(xp_list, 25),
        median=pct(xp_list, 50),
        q3=pct(xp_list, 75),
        max=float(xp_list[-1]) if xp_list else 0.0,
        mean=round(sum(xp_list) / n) if n > 0 else 0.0,
    )


@router.get("", response_model=list[UserOut])
def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
    _: User = Depends(require_teacher),
    db: Session = Depends(get_db),
):
    users = db.query(User).filter(User.role == "student").offset((page - 1) * per_page).limit(per_page).all()
    return [UserOut.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: uuid.UUID, _: User = Depends(require_teacher), db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        from fastapi import HTTPException
        raise HTTPException(404, "Usuario no encontrado")
    return UserOut.model_validate(u)

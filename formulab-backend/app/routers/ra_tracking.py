import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth_middleware import get_user, require_teacher
from app.models.user import User
from app.models.ra_tracking import RATracking
from app.schemas.ra_tracking import RATrackingOut, RATrackingListResponse, RA_LABELS

router = APIRouter(prefix="/ra-tracking", tags=["ra-tracking"])


def _build_ra_list(db: Session, user_id: uuid.UUID) -> list[RATrackingOut]:
    trackings = {t.ra_id: t for t in db.query(RATracking).filter(RATracking.user_id == user_id).all()}
    result = []
    for ra_id in range(1, 6):
        t = trackings.get(ra_id)
        result.append(RATrackingOut(
            ra_id=ra_id,
            label=RA_LABELS[ra_id],
            attempts=t.attempts if t else 0,
            successes=t.successes if t else 0,
            success_rate=(t.successes / t.attempts) if (t and t.attempts > 0) else 0.0,
            last_attempt=t.last_attempt if t else None,
        ))
    return result


@router.get("/me", response_model=RATrackingListResponse)
def get_my_ra(user: User = Depends(get_user), db: Session = Depends(get_db)):
    return RATrackingListResponse(data=_build_ra_list(db, user.id))


@router.get("/class-summary")
def class_summary(_: User = Depends(require_teacher), db: Session = Depends(get_db)):
    from app.models.user import User as UserModel
    students = db.query(UserModel).filter(UserModel.role == "student").all()
    result = []
    for s in students:
        row = {"user_id": str(s.id), "name": s.name}
        trackings = {t.ra_id: t for t in db.query(RATracking).filter(RATracking.user_id == s.id).all()}
        for ra_id in range(1, 6):
            t = trackings.get(ra_id)
            rate = (t.successes / t.attempts) if (t and t.attempts > 0) else 0.0
            row[f"ra_{ra_id}"] = round(rate * 100, 1)
        result.append(row)
    return result


@router.get("/{user_id}", response_model=RATrackingListResponse)
def get_user_ra(user_id: uuid.UUID, _: User = Depends(require_teacher), db: Session = Depends(get_db)):
    return RATrackingListResponse(data=_build_ra_list(db, user_id))

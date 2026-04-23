from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.ra_tracking import RATracking
from app.models.user import User


def update_ra_tracking(db: Session, user: User, ra_ids: list[int], score: int) -> None:
    success = score >= 70
    now = datetime.now(timezone.utc)
    for ra_id in ra_ids:
        existing = db.query(RATracking).filter(
            RATracking.user_id == user.id,
            RATracking.ra_id == ra_id,
        ).first()
        if existing:
            existing.attempts += 1
            if success:
                existing.successes += 1
            existing.last_attempt = now
        else:
            db.add(RATracking(
                user_id=user.id,
                ra_id=ra_id,
                attempts=1,
                successes=1 if success else 0,
                last_attempt=now,
            ))

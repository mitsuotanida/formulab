from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth_middleware import get_user
from app.models.user import User
from app.models.badge import Badge, UserBadge
from app.schemas.badge import BadgeOut

router = APIRouter(prefix="/badges", tags=["badges"])


@router.get("", response_model=list[BadgeOut])
def get_all_badges(user: User = Depends(get_user), db: Session = Depends(get_db)):
    all_badges = db.query(Badge).all()
    earned_ids = {ub.badge_id for ub in db.query(UserBadge).filter(UserBadge.user_id == user.id).all()}
    earned_at_map = {ub.badge_id: ub.earned_at for ub in db.query(UserBadge).filter(UserBadge.user_id == user.id).all()}
    result = []
    for b in all_badges:
        result.append(BadgeOut(
            id=b.id, name=b.name, description=b.description, icon=b.icon,
            condition_type=b.condition_type, condition_value=b.condition_value,
            xp_reward=b.xp_reward,
            earned=b.id in earned_ids,
            earned_at=earned_at_map.get(b.id),
        ))
    return result


@router.get("/mine", response_model=list[BadgeOut])
def get_my_badges(user: User = Depends(get_user), db: Session = Depends(get_db)):
    earned = db.query(Badge, UserBadge.earned_at).join(UserBadge, UserBadge.badge_id == Badge.id).filter(UserBadge.user_id == user.id).all()
    return [BadgeOut(
        id=b.id, name=b.name, description=b.description, icon=b.icon,
        condition_type=b.condition_type, condition_value=b.condition_value,
        xp_reward=b.xp_reward, earned=True, earned_at=earned_at,
    ) for b, earned_at in earned]

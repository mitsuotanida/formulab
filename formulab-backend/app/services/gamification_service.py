from datetime import date
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.badge import Badge, UserBadge
from app.models.submission import Submission

BASE_XP = {"easy": 50, "medium": 100, "hard": 200}
HINT_XP_COST = 15
STREAK_BONUS_PER_DAY = 10
MAX_STREAK_BONUS_DAYS = 5
PERFECT_SCORE_BONUS = 50
FIRST_SUBMISSION_BONUS = 25

LEVELS = [
    (0, 500, 1, "Intern"),
    (500, 1500, 2, "Junior"),
    (1500, 3500, 3, "Engineer"),
    (3500, 7500, 4, "Senior"),
    (7500, 15000, 5, "Staff"),
    (15000, None, 6, "Principal"),
]


def get_level(xp: int) -> tuple[int, str]:
    for min_xp, max_xp, level_num, level_name in LEVELS:
        if max_xp is None or xp < max_xp:
            return level_num, level_name
    return 6, "Principal"


def get_level_name(level: int) -> str:
    names = {1: "Intern", 2: "Junior", 3: "Engineer", 4: "Senior", 5: "Staff", 6: "Principal"}
    return names.get(level, "Intern")


def calculate_xp(difficulty: str, score: int, hints_used: int, streak: int, is_first: bool) -> int:
    base = BASE_XP.get(difficulty, 50)
    earned = round(base * score / 100)
    earned -= hints_used * HINT_XP_COST
    earned = max(earned, 0)
    if score == 100:
        earned += PERFECT_SCORE_BONUS
    if is_first:
        earned += FIRST_SUBMISSION_BONUS
    earned += min(streak, MAX_STREAK_BONUS_DAYS) * STREAK_BONUS_PER_DAY
    return earned


def update_streak(user: User, today: date) -> bool:
    """Updates user streak. Returns True if streak was broken."""
    if user.last_active_date is None:
        user.streak = 1
        user.last_active_date = today
        return False
    delta = (today - user.last_active_date).days
    if delta == 0:
        return False
    elif delta == 1:
        user.streak += 1
        user.last_active_date = today
        return False
    else:
        user.streak = 1
        user.last_active_date = today
        return True


def apply_xp_and_level(user: User, xp_earned: int) -> tuple[bool, str | None]:
    old_level = user.level
    user.xp += xp_earned
    new_level, new_name = get_level(user.xp)
    user.level = new_level
    leveled_up = new_level > old_level
    return leveled_up, new_name if leveled_up else None


def check_badges(db: Session, user: User, submission: Submission, exercise_type: str) -> list[Badge]:
    existing_ids = {ub.badge_id for ub in db.query(UserBadge).filter(UserBadge.user_id == user.id).all()}
    all_badges = db.query(Badge).all()
    newly_earned = []

    all_user_submissions = db.query(Submission).filter(
        Submission.user_id == user.id,
        Submission.evaluation_status == "complete",
    ).all()
    total_submissions = len(all_user_submissions)

    for badge in all_badges:
        if badge.id in existing_ids:
            continue
        earned = False
        cv = badge.condition_value

        if badge.condition_type == "first_submission":
            earned = total_submissions == 1

        elif badge.condition_type == "streak_days":
            earned = user.streak >= cv.get("threshold", 999)

        elif badge.condition_type == "xp_milestone":
            earned = user.xp >= cv.get("threshold", 999999)

        elif badge.condition_type == "score_threshold":
            perfect_count = sum(1 for s in all_user_submissions if s.score == cv.get("score", 100))
            earned = perfect_count >= cv.get("count", 1)

        elif badge.condition_type == "exercises_completed":
            diff = cv.get("difficulty")
            count = cv.get("count", 1)
            from app.models.exercise import Exercise
            matching = db.query(Submission).join(Exercise, Exercise.id == Submission.exercise_id).filter(
                Submission.user_id == user.id,
                Submission.score >= 70,
                Exercise.difficulty == diff,
            ).count()
            earned = matching >= count

        elif badge.condition_type == "type_mastery":
            tp = cv.get("type")
            min_ex = cv.get("min_exercises", 5)
            min_avg = cv.get("min_avg_score", 70)
            from app.models.exercise import Exercise
            type_subs = db.query(Submission).join(Exercise, Exercise.id == Submission.exercise_id).filter(
                Submission.user_id == user.id,
                Submission.evaluation_status == "complete",
                Exercise.type == tp,
            ).all()
            if len(type_subs) >= min_ex:
                avg = sum(s.score or 0 for s in type_subs) / len(type_subs)
                earned = avg >= min_avg

        if earned:
            db.add(UserBadge(user_id=user.id, badge_id=badge.id))
            newly_earned.append(badge)

    return newly_earned

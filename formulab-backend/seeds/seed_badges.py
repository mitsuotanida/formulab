from sqlalchemy.orm import Session
from app.models.badge import Badge


BADGES = [
    {"name": "First Blood", "description": "¡Enviaste tu primera formulación!", "icon": "first-blood", "condition_type": "first_submission", "condition_value": {}, "xp_reward": 25},
    {"name": "LP Master", "description": "Dominas la Programación Lineal (10 ejercicios con promedio ≥75%)", "icon": "lp-master", "condition_type": "type_mastery", "condition_value": {"type": "LP", "min_exercises": 10, "min_avg_score": 75}, "xp_reward": 200},
    {"name": "MIP Wizard", "description": "Dominas la Programación Entera Mixta (5 ejercicios con promedio ≥70%)", "icon": "mip-wizard", "condition_type": "type_mastery", "condition_value": {"type": "MIP", "min_exercises": 5, "min_avg_score": 70}, "xp_reward": 300},
    {"name": "NLP Explorer", "description": "Exploraste la Programación No Lineal (3 ejercicios con promedio ≥60%)", "icon": "nlp-explorer", "condition_type": "type_mastery", "condition_value": {"type": "NLP", "min_exercises": 3, "min_avg_score": 60}, "xp_reward": 150},
    {"name": "3-Day Streak", "description": "3 días consecutivos practicando", "icon": "streak-3", "condition_type": "streak_days", "condition_value": {"threshold": 3}, "xp_reward": 30},
    {"name": "Week Warrior", "description": "7 días consecutivos practicando", "icon": "streak-7", "condition_type": "streak_days", "condition_value": {"threshold": 7}, "xp_reward": 100},
    {"name": "Iron Coder", "description": "30 días consecutivos practicando", "icon": "streak-30", "condition_type": "streak_days", "condition_value": {"threshold": 30}, "xp_reward": 500},
    {"name": "Rising Star", "description": "Alcanzaste 500 XP", "icon": "rising-star", "condition_type": "xp_milestone", "condition_value": {"threshold": 500}, "xp_reward": 50},
    {"name": "Engineer Badge", "description": "Alcanzaste nivel Engineer (1500 XP)", "icon": "engineer-badge", "condition_type": "xp_milestone", "condition_value": {"threshold": 1500}, "xp_reward": 150},
    {"name": "Perfectionist", "description": "3 formulaciones perfectas (100 pts)", "icon": "perfectionist", "condition_type": "score_threshold", "condition_value": {"score": 100, "count": 3}, "xp_reward": 200},
    {"name": "Hard Mode", "description": "5 ejercicios difíciles completados (≥70%)", "icon": "hard-mode", "condition_type": "exercises_completed", "condition_value": {"difficulty": "hard", "count": 5}, "xp_reward": 400},
]


def seed_badges(db: Session) -> None:
    for badge_data in BADGES:
        existing = db.query(Badge).filter(Badge.name == badge_data["name"]).first()
        if not existing:
            db.add(Badge(**badge_data))
    db.commit()
    print(f"✓ {len(BADGES)} badges seeded")

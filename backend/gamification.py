"""
Gamification Engine — XP, Levels, and Badge System for FinMentor.
"""

from backend.database import get_streak, get_badges, award_badge, get_total_savings, get_quiz_scores

# ── Level System ──────────────────────────────────────

LEVEL_THRESHOLDS = [
    (0,    "Beginner 🌱",       1),
    (50,   "Saver 💰",          2),
    (150,  "Smart Saver 🧠",    3),
    (300,  "Investor 📈",       4),
    (500,  "Pro Investor 🚀",   5),
    (800,  "Finance Guru 🎓",   6),
    (1200, "Money Master 👑",   7),
    (1800, "Wealth Builder 🏗️", 8),
    (2500, "Financial Hero 🦸", 9),
    (3500, "Legend 🏆",         10),
]

def get_level(total_xp):
    """Return (level_number, level_name, xp_for_next_level, xp_progress_in_level)."""
    current_level = LEVEL_THRESHOLDS[0]
    next_threshold = None

    for i, (threshold, name, level_num) in enumerate(LEVEL_THRESHOLDS):
        if total_xp >= threshold:
            current_level = (threshold, name, level_num)
            if i + 1 < len(LEVEL_THRESHOLDS):
                next_threshold = LEVEL_THRESHOLDS[i + 1][0]
            else:
                next_threshold = None
        else:
            break

    level_num = current_level[2]
    level_name = current_level[1]
    current_threshold = current_level[0]

    if next_threshold:
        xp_in_level = total_xp - current_threshold
        xp_needed = next_threshold - current_threshold
        progress = xp_in_level / xp_needed
    else:
        xp_in_level = total_xp - current_threshold
        xp_needed = 0
        progress = 1.0

    return {
        "level": level_num,
        "name": level_name,
        "xp_in_level": xp_in_level,
        "xp_needed": xp_needed,
        "progress": min(progress, 1.0),
        "total_xp": total_xp,
    }

# ── Badge Definitions ────────────────────────────────

BADGE_DEFINITIONS = {
    "First Save 🌟":        {"description": "Logged your first saving", "condition": "streak >= 1"},
    "3-Day Streak 🔥":      {"description": "Saved for 3 days in a row", "condition": "streak >= 3"},
    "7-Day Streak 🔥🔥":    {"description": "Saved for 7 days in a row", "condition": "streak >= 7"},
    "14-Day Streak ⚡":     {"description": "Saved for 14 days in a row", "condition": "streak >= 14"},
    "30-Day Streak 🏆":     {"description": "Saved for 30 days in a row", "condition": "streak >= 30"},
    "Goal Achiever 🎯":     {"description": "Reached a savings goal", "condition": "manual"},
    "Quiz Starter 📖":      {"description": "Completed your first quiz", "condition": "quizzes >= 1"},
    "Quiz Master 📚":       {"description": "Completed 5 quizzes", "condition": "quizzes >= 5"},
    "₹1K Saved 💵":         {"description": "Total savings reached ₹1,000", "condition": "savings >= 1000"},
    "₹5K Saved 💰":         {"description": "Total savings reached ₹5,000", "condition": "savings >= 5000"},
    "₹10K Saved 🤑":        {"description": "Total savings reached ₹10,000", "condition": "savings >= 10000"},
    "₹50K Saved 💎":        {"description": "Total savings reached ₹50,000", "condition": "savings >= 50000"},
}

def check_and_award_badges(username):
    """Check all badge conditions and award any newly earned badges. Returns list of newly earned badge names."""
    streak_data = get_streak(username)
    current_streak = streak_data["current_streak"]
    longest_streak = streak_data["longest_streak"]
    best_streak = max(current_streak, longest_streak)

    total_savings = get_total_savings(username)
    quiz_scores = get_quiz_scores(username)
    num_quizzes = len(quiz_scores)

    existing_badges = {b["name"] for b in get_badges(username)}
    newly_earned = []

    for badge_name, badge_info in BADGE_DEFINITIONS.items():
        if badge_name in existing_badges:
            continue

        condition = badge_info["condition"]
        earned = False

        if condition == "streak >= 1" and best_streak >= 1:
            earned = True
        elif condition == "streak >= 3" and best_streak >= 3:
            earned = True
        elif condition == "streak >= 7" and best_streak >= 7:
            earned = True
        elif condition == "streak >= 14" and best_streak >= 14:
            earned = True
        elif condition == "streak >= 30" and best_streak >= 30:
            earned = True
        elif condition == "quizzes >= 1" and num_quizzes >= 1:
            earned = True
        elif condition == "quizzes >= 5" and num_quizzes >= 5:
            earned = True
        elif condition == "savings >= 1000" and total_savings >= 1000:
            earned = True
        elif condition == "savings >= 5000" and total_savings >= 5000:
            earned = True
        elif condition == "savings >= 10000" and total_savings >= 10000:
            earned = True
        elif condition == "savings >= 50000" and total_savings >= 50000:
            earned = True

        if earned:
            award_badge(username, badge_name)
            newly_earned.append(badge_name)

    return newly_earned

def get_gamification_summary(username):
    """Get complete gamification summary for a user."""
    streak_data = get_streak(username)
    level_data = get_level(streak_data["total_xp"])
    badges = get_badges(username)

    return {
        "streak": streak_data,
        "level": level_data,
        "badges": badges,
        "badge_count": len(badges),
        "total_badges": len(BADGE_DEFINITIONS),
    }

def financial_health_score(savings_percentage):
    if savings_percentage >= 40:
        return 90, "Investment Pro 🚀"
    elif savings_percentage >= 30:
        return 75, "Smart Planner 📈"
    elif savings_percentage >= 20:
        return 60, "Habit Builder 🔥"
    elif savings_percentage >= 10:
        return 40, "Beginner Saver 🌱"
    else:
        return 20, "Needs Improvement ⚠"

def financial_health_score(rate):
    if rate >= 40:
        return 90, "Investment Pro 🚀"
    elif rate >= 30:
        return 75, "Smart Planner 📈"
    elif rate >= 20:
        return 60, "Habit Builder 🔥"
    elif rate >= 10:
        return 40, "Beginner Saver 🌱"
    else:
        return 20, "Needs Improvement ⚠"

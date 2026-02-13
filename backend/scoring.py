def health_score(rate):
    if rate >= 40: return 90
    if rate >= 30: return 75
    if rate >= 20: return 60
    if rate >= 10: return 40
    return 20

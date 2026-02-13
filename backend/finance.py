def calculate_monthly_savings(income, expenses):
    return max(income - expenses, 0)

def compound_growth(monthly, rate, months):
    r = rate / 12
    if r == 0:
        return monthly * months
    return monthly * (((1 + r) ** months - 1) / r)

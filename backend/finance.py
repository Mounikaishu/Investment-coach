def calculate_monthly_savings(income, expenses):
    return max(income - expenses, 0)


def savings_rate(income, savings):
    if income == 0:
        return 0
    return (savings / income) * 100


def compound_growth(monthly_saving, annual_rate, months):
    r = annual_rate / 12
    if r == 0:
        return monthly_saving * months

    return monthly_saving * (((1 + r) ** months - 1) / r)

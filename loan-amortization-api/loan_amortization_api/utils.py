def calculate_amortization_schedule(amount, annual_interest_rate, loan_term):
    monthly_rate = annual_interest_rate / 12 / 100
    monthly_payment = amount * (monthly_rate / (1 - (1 + monthly_rate) ** -loan_term))
    schedule = []
    remaining_balance = amount

    for month in range(1, loan_term + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        schedule.append({
            "month": month,
            "remaining_balance": remaining_balance,
            "monthly_payment": monthly_payment
        })

    return schedule

def calculate_loan_summary(schedule, month):
    if month > len(schedule) or month < 1:
        raise ValueError("Invalid month")
    
    current_principal_balance = schedule[month - 1]["remaining_balance"]
    principal_paid = sum([s["monthly_payment"] - s["remaining_balance"] * (s["monthly_payment"] / schedule[0]["monthly_payment"] - 1) for s in schedule[:month]])
    interest_paid = sum([s["remaining_balance"] * (s["monthly_payment"] / schedule[0]["monthly_payment"] - 1) for s in schedule[:month]])
    
    return {
        "current_principal_balance": current_principal_balance,
        "principal_paid": principal_paid,
        "interest_paid": interest_paid
    }

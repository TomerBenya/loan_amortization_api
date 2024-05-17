from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    email: str

class LoanCreate(BaseModel):
    amount: float
    annual_interest_rate: float
    loan_term: int

class LoanSchedule(BaseModel):
    month: int
    remaining_balance: float
    monthly_payment: float

class LoanSummary(BaseModel):
    current_principal_balance: float
    principal_paid: float
    interest_paid: float

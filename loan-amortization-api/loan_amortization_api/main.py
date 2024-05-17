from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base, User, Loan
from .models import UserCreate, LoanCreate, LoanSchedule, LoanSummary
from .utils import calculate_amortization_schedule, calculate_loan_summary
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserCreate(username=db_user.username, email=db_user.email)

@app.post("/loans/", response_model=LoanCreate)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = Loan(amount=loan.amount, annual_interest_rate=loan.annual_interest_rate, loan_term=loan.loan_term, owner_id=1)  # Assuming owner_id=1 for now
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return LoanCreate(amount=db_loan.amount, annual_interest_rate=db_loan.annual_interest_rate, loan_term=db_loan.loan_term)

@app.get("/loans/schedule/{loan_id}", response_model=List[LoanSchedule])
def get_loan_schedule(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    schedule = calculate_amortization_schedule(loan.amount, loan.annual_interest_rate, loan.loan_term)
    return [LoanSchedule(month=s["month"], remaining_balance=s["remaining_balance"], monthly_payment=s["monthly_payment"]) for s in schedule]

@app.get("/loans/summary/{loan_id}/{month}", response_model=LoanSummary)
def get_loan_summary(loan_id: int, month: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    schedule = calculate_amortization_schedule(loan.amount, loan.annual_interest_rate, loan.loan_term)
    summary = calculate_loan_summary(schedule, month)
    return LoanSummary(current_principal_balance=summary["current_principal_balance"], principal_paid=summary["principal_paid"], interest_paid=summary["interest_paid"])

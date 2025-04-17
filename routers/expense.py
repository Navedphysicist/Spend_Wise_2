from models.expense import DbExpense
from fastapi import APIRouter,Depends,HTTPException,status
from schemas.expense import ExpenseBase,ExpenseDisplay,ExpenseUpdate
from sqlalchemy.orm import Session
from database import get_db
from utils.oauth2 import get_current_user
from models.user import DbUser
from typing import List


router = APIRouter(
    prefix='/expense',
    tags=['expenses']
)

@router.post('',response_model=ExpenseDisplay)
def create_income(
    expense:ExpenseBase,
    db:Session = Depends(get_db),
    current_user:DbUser = Depends(get_current_user)
    ):

    db_expense = DbExpense(**expense.model_dump(),user_id=current_user.id)

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get('',response_model=List[ExpenseDisplay])
def get_expenses(
    db:Session = Depends(get_db),
    current_user:DbUser = Depends(get_current_user)
    ):

    return db.query(DbExpense).filter(DbExpense.user_id== current_user.id).all()
   

@router.get('/total-expense',response_model=dict)
def get_total_expense(
    db:Session=Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):
    expenses = db.query(DbExpense).filter(DbExpense.user_id==current_user.id).all()
    total =  sum(expense.amount for expense in expenses)
    return {
        'total-expense':total
    }

@router.patch('/{category}',response_model=List[ExpenseDisplay])
def update_income(
    category : str,
    expense_update : ExpenseUpdate,
    db:Session = Depends(get_db),
    current_user:DbUser = Depends(get_current_user)
):
    
    expenses = db.query(DbExpense).filter(DbExpense.category == category, DbExpense.user_id == current_user.id).all()
    

    if not expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Expense not found'
        )
    
    for expense in expenses:
        if expense_update.amount is not None:
            expense.amount = expense_update.amount
        if expense_update.date is not None:
            expense.date = expense_update.date
        if expense_update.is_recurring is not None:
            expense.is_recurring = expense_update.is_recurring
        if expense_update.category is not None:
            expense.category = expense_update.category

    db.commit()
    for expense in expenses:
        db.refresh(expense)
    return expenses




@router.delete('/{category}')
def delete_expense(
    category : str,
    db:Session = Depends(get_db),
    current_user:DbUser = Depends(get_current_user)
):
    expenses = db.query(DbExpense).filter(DbExpense.category == category, DbExpense.user_id == current_user.id).all()
    if not expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Income not found'
    )

    for expense in expenses:
        db.delete(expense)
    
    db.commit()
    return {
        'message' : 'Deleted Successfully'
    }


  





    
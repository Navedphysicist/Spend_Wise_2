from models.income import DbIncome
from fastapi import APIRouter,Depends,HTTPException,status
from schemas.income import IncomeDisplay,IncomeBase,IncomeUpdate
from sqlalchemy.orm import Session
from database import get_db
from utils.oauth2 import get_current_user
from models.user import DbUser
from typing import List,Optional


router = APIRouter(
    prefix='/income',
    tags=['incomes']
)

@router.post('',response_model=IncomeDisplay)
def create_income(
    income:IncomeBase,
    db:Session = Depends(get_db),
    current_user:DbUser = Depends(get_current_user)
    ):

    db_income = DbIncome(**income.model_dump(),user_id=current_user.id)

    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

@router.get('',response_model=List[IncomeDisplay])
def get_income(
    source : Optional[str] = None,
    db:Session = Depends(get_db),
    current_user:DbUser = Depends(get_current_user)
    ):

    query = db.query(DbIncome).filter(DbIncome.user_id== current_user.id)
    if source:
        query = query.filter(DbIncome.source.ilike(f"%{source}%"))
    return query.all()

@router.get('/total-income',response_model=dict)
def get_total_income(
    db:Session=Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):
    incomes = db.query(DbIncome).filter(DbIncome.user_id==current_user.id).all()
    total =  sum(income.amount for income in incomes)
    return {
        'total-income':total
    }

@router.patch('/{income_id}',response_model=IncomeDisplay)
def update_income(
    income_id : int,
    income_update : IncomeUpdate,
    db:Session = Depends(get_db),
    current_user:DbUser = Depends(get_current_user)
):
    db_income = db.query(DbIncome).filter(DbIncome.id == income_id, DbIncome.user_id == current_user.id).first()

    if not db_income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Income not found'
        )


    udpated_data = income_update.model_dump(exclude_unset=True)
    for key , value in udpated_data.items():
        setattr(db_income,key,value)

    db.commit()
    db.refresh(db_income)
    return db_income

@router.delete('/{income_id}')
def delete_income(
    income_id : int,
    db:Session = Depends(get_db),
    current_user:DbUser = Depends(get_current_user)
):
    db_income = db.query(DbIncome).filter(DbIncome.id == income_id, DbIncome.user_id == current_user.id).first()
    if not db_income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Income not found'
    )

    db.delete(db_income)
    db.commit()
    return {
        'message' : 'Deleted Successfully'
    }


  





    
from pydantic import BaseModel
from datetime import date as date_type
from typing import Optional

# ExpenseBase => get data for create Expense from User
class ExpenseBase(BaseModel):
    amount : float
    date : date_type
    category : str
    is_recurring : bool = False


# ExpenseUpdate => Update from User
class ExpenseUpdate(BaseModel):
    amount : Optional[float] = None
    date : Optional[date_type] = None
    category : Optional[str] = None
    is_recurring : Optional[bool] = None


# ExpenseDispay => Return data to the user
class ExpenseDisplay(ExpenseBase):
    id : int
    user_id : int

    class Config:
        from_attributes = True

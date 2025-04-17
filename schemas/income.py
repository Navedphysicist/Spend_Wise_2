from pydantic import BaseModel
from datetime import date as date_type
from typing import Optional

# IncomeBase => get data for create Income from User
class IncomeBase(BaseModel):
    amount : float
    date : date_type
    source : str
    is_recurring : bool = False


# IncomeUpdate => Update from User
class IncomeUpdate(BaseModel):
    amount : Optional[float] = None
    date : Optional[date_type] = None
    source : Optional[str] = None
    is_recurring : Optional[bool] = None


# IncomeDispay => Return data to the user
class IncomeDisplay(IncomeBase):
    id : int
    user_id : int

    class Config:
        from_attributes = True

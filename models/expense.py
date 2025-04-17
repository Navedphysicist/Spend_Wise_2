from database import Base
from sqlalchemy import Column,Integer,Float,Date,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship


class DbExpense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer,primary_key=True,index=True)
    amount = Column(Float,nullable=False)
    date = Column(Date,nullable=False)
    category = Column(String,nullable=False)
    is_recurring = Column(Boolean,default=False)

   #Foreign Key
    user_id = Column(Integer,ForeignKey('users.id'))

    user = relationship('DbUser',back_populates='expenses')


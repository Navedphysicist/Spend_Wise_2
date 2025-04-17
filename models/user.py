from database import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,nullable=False)
    hashed_password = Column(String)

    #Relationship
    incomes = relationship('DbIncome',back_populates='user')
    expenses = relationship('DbExpense',back_populates='user')
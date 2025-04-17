from fastapi import FastAPI
from database import Base, engine
from routers import auth, income, expense


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='SpendWise API',
    description='Finance Management API',
    version='2.0.0'
)

app.include_router(auth.router)
app.include_router(income.router)
app.include_router(expense.router)


@app.get('/')
def root():
    return {'message': 'Welcome to Spendwise API.'}

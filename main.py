from fastapi import FastAPI
from database import Base, engine
from routers import auth
from models import user, income, expense  # Import all models


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='SpendWise API',
    description='Finance Management API',
    version='2.0.0'
)

app.include_router(auth.router)


@app.get('/')
def root():
    return {'message': 'Welcome to Spendwise API.'}

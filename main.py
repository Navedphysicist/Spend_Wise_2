from fastapi import FastAPI
from database import Base,engine


Base.metadata.create_all(bind = engine)

app = FastAPI(
    title='SpendWise API',
    description='Finance Management API',
    version='2.0.0'
)


@app.get('/')
def root():
    return {'message':'Welcome to Spendwise API.'}
from models.user import DbUser
from fastapi import APIRouter,Depends,HTTPException,status
from schemas.user import Token,UserBase
from sqlalchemy.orm import Session
from database import get_db
from utils.hash import get_password_hash,verify_password
from utils.auth_token import create_acess_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/signup',response_model=Token)
def create_user(user:UserBase,db:Session = Depends(get_db)):
   db_user =  db.query(DbUser).filter(DbUser.username == user.username).first()

   if db_user:
     raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Username already registered'
    )
   
   hashed_password = get_password_hash(user.password)

   db_user = DbUser(username=user.username,hashed_password=hashed_password)

   db.add(db_user)
   db.commit()
   db.refresh(db_user)

   access_token = create_acess_token(data = {'sub':user.username})
   return {
      'access_token' : access_token,
      'token_type' : 'bearer'
   }


@router.post('/login',response_model=Token)
def login(
   form_data : OAuth2PasswordRequestForm = Depends(),
   db:Session = Depends(get_db)
):
   
   user = db.query(DbUser).filter(DbUser.username == form_data.username).first()

   if not user or not verify_password(form_data.password,user.hashed_password):
       raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password'
    )
   access_token = create_acess_token(data = {'sub':user.username})

   return {
      'access_token' : access_token,
      'token_type' : 'bearer'
   }
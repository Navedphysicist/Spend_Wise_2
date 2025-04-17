from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt,JWTError
from utils.auth_token import SECRET_KEY
from models.user import DbUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_current_user(token:str = Depends(oauth2_scheme),db:Session= Depends(get_db)):
    credentials_excpetion = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials'
         )
    try:
        payload =  jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        username = payload.get('sub')
        if username is None:
            raise "username not present"
    except JWTError:
        raise credentials_excpetion
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if user is None:
        raise 'user not present'
    return user
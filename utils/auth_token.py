from typing import Optional
from datetime import datetime, timedelta,timezone
from jose import jwt,JWTError
from fastapi import HTTPException,status

SECRET_KEY = 'MY_SPENDWISE_SECRET_KEY'


def create_acess_token(data:dict,expires_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm='HS256')
    return encoded_jwt


def verify_token(token:str):

    try:
        payload =  jwt.decode(token,SECRET_KEY,algorithms='HS256')
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )







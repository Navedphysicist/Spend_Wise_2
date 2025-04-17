from pydantic import BaseModel

class UserBase(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    acess_token : str
    token_type : str
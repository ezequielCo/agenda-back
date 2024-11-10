import secrets
from typing_extensions import Annotated
from fastapi import FastAPI,HTTPException, Depends,status,APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials,OAuth2PasswordBearer, OAuth2PasswordRequestForm
from modelos.users import Users
from database import engine,SessionLocal,Base
from pydantic  import BaseModel ,Field
from typing import Union
from sqlalchemy.orm import Session
from datetime import date, time,datetime,timedelta,timezone
from fastapi.middleware.cors import CORSMiddleware
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from typing_extensions import Annotated



router = APIRouter()
security = HTTPBasic()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30





class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None



class UserBase(BaseModel):
    name : str
    username: str
    email: str  
    password: str 
      

class UserInDB(UserBase):
    hashed_password: str

def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_dependency = Annotated[Session,Depends(get_db)]

# to get a string like this run:
# openssl rand -hex 32




@router.get('/get/users',tags=["Users"])
async def listevnetos(db:db_dependency):
    usuario =db.query(Users).all()
    if usuario is None:
            return HTTPException(status_code=404,detail='Evento no encontrado')
        
    return usuario #comento
        

@router.get('/login',tags=["Users"])
def read_current_user(username: 'str'):
    return {"username": username}








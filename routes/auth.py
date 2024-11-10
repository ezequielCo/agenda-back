from  datetime import timedelta,datetime
from typing import Annotated
from typing_extensions import Annotated
from fastapi import FastAPI,HTTPException, Depends,status,APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials,OAuth2PasswordBearer, OAuth2PasswordRequestForm
from modelos.users import Users,UserRoles,Roles
from database import engine,SessionLocal,Base
from pydantic  import BaseModel ,Field,field_validator, EmailStr 
from typing import Union
from sqlalchemy.orm import Session
from datetime import date, time,datetime,timedelta,timezone

from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError


router = APIRouter(

    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


##esote es le modelo de autheticacion ppero no lo voy a usar 
#ahorita de moento solo con el caso de authenticacion
class UserBase(BaseModel):
    username: str 
    password: str 
    name :str 
    username :str 
    email :EmailStr

class UserLog(BaseModel):
    username: str 
    password: str 
  


class UserAuth(BaseModel):
    username: str
    id: int


class Token(BaseModel):
    user_id: int
    access_token: str
    token_type: str

def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_dependency = Annotated[Session,Depends(get_db)]

#Validate Emails
def verify_email_exists(db: Session, email: EmailStr) -> bool:
    user = db.query(Users).filter(Users.email == email).first()
    return user is not None

#validate Users 
def verify_username_exists(db: Session, username: str) -> bool:
    user = db.query(Users).filter(Users.username == username).first()
    return user is not None


# Here registred 
@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:UserBase,roles: list[int]):
    try:
            """
            this funtion receives the  request sent from  register users form and will saved on databes,use the tables users,roles, roles_users  , it  function should validate if user exist,if user email exits and rol_id exits,so return errors
            """        
            if verify_email_exists(db, create_user_request.email):
                return {"data": "error" ,"status_code":400,"detail": "Correo electronico  ya existente."}
            

            if verify_username_exists(db, create_user_request.username):
                return {"data": "error" ,"status_code":400,"detail": "Usuario ya existente"}
                #return HTTPException(status_code=400, detail="Email already exists")
            
            create_user_model =Users(
                  name = create_user_request.name,
                  username=create_user_request.username,
                  email = create_user_request.email,
                  hashed_password = bcrypt_context.hash(create_user_request.password),
                
                  
            )
            #save users
            db.add(create_user_model)
            db.commit()

            if create_user_model.id is not None: #e
                print(create_user_model.id)
                for rol_id in roles:
                    # save the users whit the id_rol
                    role_usuario = UserRoles(usuario_id=create_user_model.id, rol_id=rol_id)
                    db.add(role_usuario)
           
                db.commit()
                return {"data": "success" ,"status_code":200,"details": "Registro aplicado con exito"}
            else:
                return {"data": "error" ,"status_code":401,"details": "Error al intentar aplicar registo"}
               # db.add(role_usuario)

            #db.add(create_user_model)
            #db.add(create_user_model)
            
            #db.commit()
    except Exception as e:
        print(f"Error al crear el usuario: {str(e)}")
        
        raise ValueError("Error al crear el usuario. Por favor, verifica los datos.")
    

    




@router.post("/token")
async def login_for_access_token(db:db_dependency,form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#async def login_for_access_token(form_data:UserLog,db: db_dependency):

    user = authenticate_user(form_data.username,form_data.password,db)
   # print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token =create_access_token(user.username,user.id,timedelta(minutes=20))
    #print(user)
    #return user
    return {"user_id": user.id,"access_token": token, "token_type": "bearer"}
    


"""

@router.post("/token")
async def login_for_access_token(form_data: UserLog = Depends(),db):

    valu = {'form':form_data.username,'formv':form_data.password} 
    print(valu)
    user = authenticate_user(form_data.username,form_data.password,db)
   # print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could no validate user.')
        
    token =create_access_token(user.username,user.id,timedelta(minutes=20))
    print(token)
    return {"user_id": user.id,"access_token": token, "token_type": "bearer"}

"""


def authenticate_user( username: str, password: str,db):
 
    user = db.query(Users).filter(Users.username == username ).first()
    
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username:str, user_id:int,expires_delta:timedelta):
     encode ={'sub':username , 'id' :user_id}
     experies =datetime.now() + expires_delta
     expires_str = experies.isoformat()
     encode.update({'exp:' :expires_str})
 
     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        #print(username)
        #print(user_id)
      
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
            )
        ##aqui tengo el usuario id , puedo hacee un consulta mejor que me permita obtener los balores completos del usuario
        
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    
def get_current_active_user(current_user: dict = Depends(get_current_user)):
    return current_user
    
@router.get("/me", response_model=UserAuth)
async def read_users_me(current_user: UserAuth = Depends(get_current_user)):
    
    """esto unicamanete retorna el ide de susuario y username , con esto puedo hace una consulta desde el frot
     debo traer 1 datos del usuario , si esta activo o no , y los roles y permisos
    Quizas hay una forma mas sencilla de momento esta es la unica 
    """
    return current_user

def generate_new_token(user: UserAuth):
    encoded_jwt = jwt.encode({"sub": user["username"], "id": user["id"]}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}





@router.post("/logout")
async def logout(current_user: UserAuth = Depends(get_current_user), db: Session = Depends(get_db)):
    # Expirar el token actual
    access_token_expires = datetime.utcnow() + timedelta(minutes=15)
    
    # Actualizar la base de datos con el token expirado
    db.query(Users).filter(Users.id == current_user['id']).update({
        "access_token_expires": access_token_expires
    })
    db.commit()

    return {"message": "Logged out successfully", "new_token": generate_new_token(current_user)}
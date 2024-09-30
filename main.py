from fastapi import FastAPI,HTTPException, Depends,status
from pydantic  import BaseModel ,Field
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from datetime import date, time,datetime  
from fastapi.middleware.cors import CORSMiddleware
from routes import events,contactos



app = FastAPI()
app.include_router(events.router)
app.include_router(contactos.router)
origins = [
    "http://localhost:3000",
    "http://localhost:3000/api",  # Example path for your API endpoint
    "http://localhost:3000/dashboard",  # Example path for a dashboard route
    "http://localhost:3000/home",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)# Pass the app instance

models.Base.metadata.create_all(bind=engine)


@app.get('/',tags=['home'])
def home():
    return {"Hello": "World"}

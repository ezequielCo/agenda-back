from fastapi import FastAPI,HTTPException, Depends,status

from pydantic  import BaseModel ,Field
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from datetime import date, time,datetime  


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class EventoBase(BaseModel):
    evento : str
    description: str
    fecha_evento: date  
    hora_evento: time   


def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@app.get("/",tags=['Home'])
def read_root():
    return {"Hello": "World"}


@app.post('/eventos',tags=["Eventos"],status_code=status.HTTP_201_CREATED)
async def crear_evento(evento: EventoBase ,db:db_dependency):
     db_evento = models.Events(**evento.dict())
     db.add(db_evento)
     db.commit()

     return HTTPException(status_code=200,detail='Registrado con Exito.')

@app.get("/envento/{evento_id}",tags=["Eventos"],status_code=status.HTTP_200_OK)
async def get_evento(evento_id:int,db: db_dependency):
     mi_evento =db.query(models.Events).filter(models.Events.id == evento_id ).first()
     if mi_evento is None:
          return HTTPException(status_code=404,detail='Evento no encontrado')
     
     return mi_evento #comento



@app.delete('/delete/evento/{evento_id}',tags=["Eventos"],status_code=status.HTTP_200_OK)
async def delete(evento_id:int,db: db_dependency):

     mi_evento = db.query(models.Events).where(models.Events.id == evento_id ).first()
     if mi_evento is None:
          raise HTTPException(status_code=404,detail= 'Evento no encontrado')
     db.delete(mi_evento)
     db.commit()

     return HTTPException(status_code=200,detail= 'Evento Eliminado')



@app.put('/update/evento/{evento_id}',tags=["Eventos"],response_model=EventoBase,status_code=status.HTTP_200_OK)
async def updateEvent(evento_id:int, response_to_update : EventoBase,db: db_dependency):
    try:
        """
        Updates an existing event record in the database.

        - Path parameter: `evento_id` (int) - The unique ID of the event to be updated.
        - Request body: `updated_data` (Events) - A JSON object containing the updated event details.
        - Returns: The updated event record (Events) upon successful update.
        - Raises:
            - HTTPException with status code 404 (Not Found) if the event with the provided ID is not found.
        """
          
    
        mi_evento_update = db.query(models.Events).where(models.Events.id == evento_id ).first()
                
        if mi_evento_update is None:
                    # if Evento this empty return 404
            return  HTTPException(status_code=404,detail="Event not found")
                
                #go to update the evento
        mi_evento_update.evento = response_to_update.evento
        mi_evento_update.description = response_to_update.description
        mi_evento_update.fecha_evento = response_to_update.fecha_evento
        mi_evento_update.hora_evento = response_to_update.hora_evento
                
        # execute update
        db.commit()
        db.refresh(mi_evento_update)  # Actualiza el objeto en la sesión
 
        return mi_evento_update
                
    
    except Exception as e:
    # Log the error for troubleshooting
        error = f"Error updating event: {e}"
    raise HTTPException(status_code=500, detail=f"Internal server error:{error}")
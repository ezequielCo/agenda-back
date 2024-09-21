from sqlalchemy import Boolean,String,Date,Time,Column,Integer
from database import Base



class Events(Base):


    __tablename__ ='events'

    id = Column(Integer,primary_key=True,index=True)
    evento = Column(String(25),unique=True)
    description = Column(String(100))
    fecha_evento = Column(Date)
    hora_evento = Column(Time)
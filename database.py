import sqlalchemy
from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker 
import sqlalchemy.ext.declarative
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'mysql+pymysql://root@localhost:3306/envents'

# Crear el engine
engine = create_engine(URL_DATABASE)

# Configurar SessionLocal
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Crear Base
Base = declarative_base()


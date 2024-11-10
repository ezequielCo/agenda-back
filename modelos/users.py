from sqlalchemy import Boolean, String, Date, Time, Column, Integer, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base




class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)  # Store hashed password
    created_at = Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow)
    last_login_at = Column(DateTime)
    role = Column(String(20))  # Example: "admin", "user"
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    reset_password_token = Column(String(120))
    access_token_expires = Column(DateTime, nullable=True)

   
    roles = relationship("Roles", secondary="roles_users", back_populates="users") 



##Tabla Roles

class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(25), unique=True)
    is_active = Column(Boolean, default=True)
    ##permisos = relationship("Permisos", secondary="roles_permisos", back_populates="roles")
    users = relationship("Users", secondary="roles_users", back_populates="roles")


##tabla permisos

class UserRoles(Base):
    __tablename__ = "roles_users"
    usuario_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)



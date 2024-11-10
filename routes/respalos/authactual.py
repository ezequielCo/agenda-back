##tabla permisos
class Permisos(Base):
    __tablename__ = 'permisos'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), unique=True)
    descripcion = Column(String(25), unique=True)
    slug = Column(String(25), unique=True)
    is_active = Column(Boolean, default=True)
  #  roles = relationship("Roles", secondary="roles_permisos", back_populates="permisos")



class RolesPermisos(Base):
    __tablename__ = "roles_permisos"
    rol_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permiso_id = Column(Integer, ForeignKey("permisos.id"), primary_key=True)
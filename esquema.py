
from datetime import date
from pydantic import BaseModel

class Tarea_esquema (BaseModel):
    id: int
    titulo: str
    descripcion:str
    fecha_vencimiento : date

class Tarea_actualizada(BaseModel):
    titulo: str
    descripcion:str
    fecha_vencimiento : date

class Tarea_actualizada_patch(BaseModel):
    titulo: str = None
    descripcion:str = None
    fecha_vencimiento : date = None
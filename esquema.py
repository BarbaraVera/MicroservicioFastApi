
from datetime import date
from pydantic import BaseModel

class Tarea_esquema (BaseModel):
    titulo: str
    descripcion:str
    fecha_vencimiento : date

class Lista_tareas (BaseModel):
    id: int
    titulo: str
    descripcion:str
    fecha_vencimiento : date
    estado : str

class Tarea_actualizada(BaseModel):
    titulo: str
    descripcion:str
    fecha_vencimiento : date

class Tarea_actualizada_patch(BaseModel):
    titulo: str = None
    descripcion:str = None
    fecha_vencimiento : date = None

class Estado_tarea(BaseModel):
    estado:str

class Filtro_tarea(BaseModel):
    estado : str = None
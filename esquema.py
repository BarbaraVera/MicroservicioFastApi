
from datetime import date
from pydantic import BaseModel

class Tarea_esquema (BaseModel):
    titulo: str
    descripcion:str
    fecha_vencimiento : date
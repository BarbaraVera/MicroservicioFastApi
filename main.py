from typing import List
from fastapi import FastAPI
from basededatos import SessionLocal, Tarea
from esquema import Tarea_esquema

app = FastAPI()

#creo tareas
@app.post("/crear/", response_model=Tarea_esquema)
def crear_tarea(tarea: Tarea_esquema):
    conexion = SessionLocal()

    tarea_nueva = Tarea(
        titulo=tarea.titulo,
        descripcion = tarea.descripcion,
        fecha_vencimiento = tarea.fecha_vencimiento
    )

    conexion.add(tarea_nueva)
    conexion.commit()
    conexion.refresh(tarea_nueva)
    conexion.close()

    return tarea

#obtengo las tareas
@app.get("/tareas/", response_model=List[Tarea_esquema])
def obtener_tareas():
    conexion = SessionLocal()
    tareas = conexion.query(Tarea).all()
    conexion.close()
    return tareas
from typing import List
from fastapi import Body, FastAPI, HTTPException
from basededatos import SessionLocal, Tarea
from esquema import Tarea_esquema, Tarea_actualizada, Tarea_actualizada_patch, Lista_tareas, Estado_tarea, Filtro_tarea

app = FastAPI()

#creo tareas
@app.post("/crear/", response_model=Tarea_esquema)
def crear_tarea(tarea: Tarea_esquema):
    conexion = SessionLocal()

    tarea_nueva = Tarea(
        titulo=tarea.titulo,
        descripcion = tarea.descripcion,
        fecha_vencimiento = tarea.fecha_vencimiento,
        estado = "Pendiente"
    )

    conexion.add(tarea_nueva)
    conexion.commit()
    conexion.refresh(tarea_nueva)
    conexion.close()

    return tarea

#obtengo las tareas
@app.get("/tareas/", response_model=List[Lista_tareas])
def obtener_tareas():
    conexion = SessionLocal()
    tareas = conexion.query(Tarea).all()
    conexion.close()
    return tareas

#eliminar tarea
@app.delete("/tareas/{tarea_id}/")
def eliminar_tarea(tarea_id: int):
    conexion = SessionLocal()
    tarea = conexion.query(Tarea).filter(Tarea.id == tarea_id).first()

    if tarea is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="No existe")
    
    conexion.delete(tarea)
    conexion.commit()
    conexion.close()

    return {"message": "La tarea se ha eliminado"}

#actualizar tareas
@app.put("/tareas/{tarea_id}/")
def actualizar_tarea(tarea_id: int, tarea_actualizada: Tarea_actualizada):
    conexion = SessionLocal()
    tarea = conexion.query(Tarea).filter(Tarea.id == tarea_id).first()

    if tarea is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="La tarea no existe")
    
    tarea.titulo = tarea_actualizada.titulo
    tarea.descripcion = tarea_actualizada.descripcion
    tarea.fecha_vencimiento = tarea_actualizada.fecha_vencimiento

    conexion.commit()
    conexion.close()

    return {"message": "Tarea actualizada correctamente"}

#actualizar con patch
@app.patch("/tareas/{tarea_id}/")
def actualizar_tarea_patch(tarea_id: int, tarea_actualizada: Tarea_actualizada_patch):
    conexion = SessionLocal()
    tarea = conexion.query(Tarea).filter(Tarea.id == tarea_id).first()

    if tarea is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="La tarea no existe")
    
    if tarea_actualizada.titulo is not None:
        tarea.titulo = tarea_actualizada.titulo
    if tarea_actualizada.descripcion is not None:
        tarea.descripcion = tarea_actualizada.descripcion
    if tarea_actualizada.fecha_vencimiento is not None:
        tarea.fecha_vencimiento = tarea_actualizada.fecha_vencimiento
    
    conexion.commit()
    conexion.close()

    return  {'message': 'tarea actualizada'}

#Actualizar estado
@app.put("/tareas/{tarea_id}/estado/")
def cambiar_estado(tarea_id:int, estado: Estado_tarea):
    conexion= SessionLocal()
    tarea = conexion.query(Tarea).filter(Tarea.id == tarea_id).first()

    if tarea is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="No encontrado")
    
    if estado.estado not in ["Completada"]:
        conexion.close()
        raise HTTPException(status_code=404, detail="No existe ese estado")
    
    tarea.estado = estado.estado

    conexion.commit()
    conexion.close()

    return {"message": "Estado actualizado"}
    
#Buscar por estado
@app.get("/tareas/estado/")
def obtener_tareas_filtradas(filtros: Filtro_tarea = Body(None)):
    db = SessionLocal()
    buscar = db.query(Tarea)
    
    if filtros.estado:
        buscar = buscar.filter(Tarea.estado == filtros.estado)
    
    tareas = buscar.all()
    
    db.close()
    
    return {"tareas": tareas}
from typing import List
from fastapi import Body, FastAPI, HTTPException, Query
from basededatos import SessionLocal, Tarea
from esquema import Tarea_esquema, Tarea_actualizada, Tarea_actualizada_patch, Lista_tareas, Estado_tarea, Filtro_tarea

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Microservicio FastAPI"}

#creo tareas
@app.post("/crear/", response_model=Tarea_esquema)
def crear_tarea(tarea: Tarea_esquema):
    conexion = SessionLocal()
    
    try:
        tarea_nueva = Tarea(
            titulo=tarea.titulo,
            descripcion=tarea.descripcion,
            fecha_vencimiento=tarea.fecha_vencimiento,
            estado="Pendiente"
        )
        conexion.add(tarea_nueva)
        conexion.commit()
        conexion.refresh(tarea_nueva)
    except Exception as e:
        # Manejar excepciones específicas aquí
        conexion.rollback()
        raise HTTPException(status_code=500, detail="Error al crear la tarea")
    finally:
        conexion.close()

    return tarea


#obtengo las tareas
@app.get("/tareas/", response_model=List[Lista_tareas])
def obtener_tareas():
    conexion = SessionLocal()

    try:
        tareas = conexion.query(Tarea).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener las tareas")
    finally:
        conexion.close()

    return tareas


#eliminar tarea
@app.delete("/tarea/{tarea_id}/")
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
@app.put("/tarea/{tarea_id}/")
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
@app.patch("/tarea/{tarea_id}/")
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
@app.put("/tarea/{tarea_id}/estado/")
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
@app.get("/tareas/por_estado/")
def buscar_tareas_por_estado(estado: str = Query(None, description="Filtrar tareas por estado")):
    conexion = SessionLocal()
    
    if estado is not None:
        tareas = conexion.query(Tarea).filter(Tarea.estado == estado).all()
    else:
        tareas = conexion.query(Tarea).all()
    
    conexion.close()
    
    return tareas
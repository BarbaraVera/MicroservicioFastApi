from fastapi.testclient import TestClient
import pytest

from main import app
client = TestClient(app)
#Test de crear
def test_crear_tarea():
    datos_tarea = {
    "titulo": "Tarea test",
    "descripcion": "descripcion test",
    "fecha_vencimiento": "2023-10-12",
    }
    response = client.post("/crear/", json=datos_tarea)
    assert response.status_code == 200
    tarea_creada = response.json()
    assert tarea_creada["titulo"] == "Tarea test"

def test_creacion_tarea_sin_titulo():
    datos_tarea = {
        "descripcion": "Descripción tarea de prueba",
        "fecha_vencimiento": "2023-10-12"
    }
    response = client.post("/crear/", json=datos_tarea)
    assert response.status_code == 422  


#Test de obtener
def test_obtener_tarea():
    response = client.get("/tareas/")
    assert response.status_code == 200
    tareas = response.json()
    assert isinstance(tareas, list)

#Test de eliminar
def test_eliminar_tarea():
    tarea_id_existente = 5 

    response = client.delete(f"/tarea/{tarea_id_existente}/")

    assert response.status_code == 200
    assert response.json() == {"message": "La tarea se ha eliminado"}

#Test de actualizar put
def test_actualizar_tarea():
    id_existente = 3
    tarea_actualizada = {
        "titulo": "Tarea actualizada",
        "descripcion": "Descripción actualizada",
        "fecha_vencimiento": "2023-12-31"
    }
    response = client.put(f"/tarea/{id_existente}/", json=tarea_actualizada)
    assert response.status_code == 200
    assert response.json() == {"message": "Tarea actualizada correctamente"}

#Test de actualizar patch
def test_actualizar_tarea_patch():
    id_existente = 2
    tarea_actualizada = {
        "descripcion": "Descripción actualizada patch",
    }
    response = client.patch(f"/tarea/{id_existente}/", json=tarea_actualizada)
    assert response.status_code == 200
    assert response.json() == {"message": "tarea actualizada"}

def test_actualizar_tarea_patch_no_encontrada():
    tarea_id_no_existente = 9999  
    tarea_actualizada = {
        "titulo": "Nuevo Título tarea",
        "descripcion": "Nueva Descripción tarea",
        "fecha_vencimiento": "2023-12-31"
    }

    response = client.patch(f"/tarea/{tarea_id_no_existente}/", json=tarea_actualizada)

    assert response.status_code == 404
    assert response.json() == {"detail": "La tarea no existe"}

#Test de cambiar estado
def test_cambiar_estado():
    id_existente = 4
    estado_valido = {"estado": "Completada"}

    response = client.put(f"/tarea/{id_existente}/estado/", json=estado_valido)

    assert response.status_code == 200
    assert response.json() == {"message": "Estado actualizado"}

def test_cambiar_estado_no_encontrado():
    tarea_id_no_existente = 9999 
    estado_valido = {"estado": "Completada"}

    response = client.put(f"/tarea/{tarea_id_no_existente}/estado/", json=estado_valido)

    assert response.status_code == 404
    assert response.json() == {"detail": "No encontrado"}

def test_cambiar_estado_invalido():
    tarea_id_existente = 4  
    estado_invalido = {"estado": "Invalido"}

    response = client.put(f"/tarea/{tarea_id_existente}/estado/", json=estado_invalido)

    assert response.status_code == 404
    assert response.json() == {"detail": "No existe ese estado"}

#Obtener tareas por estado
def test_buscar_tareas_por_estado():
    response = client.get("/tareas/por_estado/")
    assert response.status_code == 200  
    tareas = response.json()
    assert len(tareas) > 0 

    response = client.get("/tareas/por_estado/?estado=Completada")
    assert response.status_code == 200 
    tareas_completadas = response.json()
    assert len(tareas_completadas) > 0  


def test_buscar_tareas_por_estado_sin_estado():
    response = client.get("/tareas/por_estado/")
    assert response.status_code == 200  
    tareas = response.json()
    assert len(tareas) > 0 

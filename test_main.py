from fastapi.testclient import TestClient

from main import app
client = TestClient(app)

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

def test_obtener_tarea():
    response = client.get("/tareas/")
    assert response.status_code == 200
    tareas = response.json()
    assert isinstance(tareas, list)

def test_eliminar_tarea():
    tarea_id_existente = 7 

    response = client.delete(f"/tarea/{tarea_id_existente}/")

    assert response.status_code == 200
    assert response.json() == {"message": "La tarea se ha eliminado"}



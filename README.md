# MicroservicioFastApi
Este es un proyecto de microservicio con FastAPI para gestionar tareas. Puedes crear, leer, actualizar y eliminar tareas a través de una API REST. Los datos se almacenaran en una base de datos sqlite.

## Requisitos

- Python 3.7+
- Dependencias adicionales se encuentran en `requirements.txt`

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/BarbaraVera/MicroservicioFastApi.git

2. Instala dependencias:
    pip install -r requirements.txt

## Uso

1. Ejecuta la aplicación:
    uvicorn main:app --reload

    La aplicación está disponible en http://127.0.0.1:8000/

2. Accede a la documentación Swagger:
    Se accede a traves de  http://127.0.0.1:8000/docs para explorar y probar los endpoints API.

## ENDPOINTS
El proyecto incluye los siguientes endpoints:

1. POST /crear/: Crea una nueva tarea.
2. GET /tareas/: Obtiene la lista de todas las tareas.
3. DELETE /tarea/{tarea_id}/: Elimina una tarea por su ID.
4. PUT /tarea/{tarea_id}/: Actualiza una tarea por su ID.
5. PATCH /tarea/{tarea_id}/: Actualiza parcialmente una tarea por su ID.
6. PUT /tarea/{tarea_id}/estado/: Cambia el estado de una tarea a "Completada".
7. GET /tareas/por_estado/: Filtra tareas por estado.("Pendiente" o "Completada")



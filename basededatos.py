from fastapi import FastAPI
from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

DATABASE_URL = "sqlite:///basededatos.db"

engine = create_engine(DATABASE_URL)
#aqui creo objetos de sesion que permite realizar operaciones en mi bd
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
Base = declarative_base()

class Tarea(Base):
    __tablename__ = "tareas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    descripcion = Column(String)
    fecha_vencimiento = Column(Date)

Base.metadata.create_all(bind=engine)
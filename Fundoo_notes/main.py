from fastapi import FastAPI
import model
from DB.database import engine
from routes import router

# Create tables
model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fundoo Notes",
    description="A FastAPI backend for managing notes and labels",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Fundoo Notes API is running!"}

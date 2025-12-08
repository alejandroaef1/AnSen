from fastapi import FastAPI
from pydantic import BaseModel
from gradio_client import Client
import sqlite3
import uvicorn

app = FastAPI()

# Conectar al modelo de Hugging Face
client = Client("https://aaesfr-clasificador-de-opiniones.hf.space")

class ReviewRequest(BaseModel):
    id_cliente: int
    reseña: str

@app.post("/analizar")
def analizar_sentimiento(data: ReviewRequest):
    resultado, estrellas = client.predict(
        data.reseña,
        api_name="/predict"
    )

    # Conectar a la base de datos
    conn = sqlite3.connect("reviews.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO opiniones (id_cliente, critica, resultado, estrellas)
        VALUES (?, ?, ?, ?)
    """, (data.id_cliente, data.reseña, resultado, int(estrellas)))
    conn.commit()
    conn.close()

    return {
        "resultado": resultado,
        "estrellas": estrellas
    }

@app.get("/")
def read_root():
    return {"message": "API de análisis de reseñas funcionando"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
import sqlite3

conn = sqlite3.connect("reviews.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS textos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        critica TEXT NOT NULL,
        resultado TEXT NOT NULL,
        estrellas INTEGER NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()

print("Base de datos 'reviews.db' creada exitosamente!")
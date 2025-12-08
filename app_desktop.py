import tkinter as tk
import requests
from tkinter import messagebox
import threading
import subprocess
import time
import os

API_URL = "http://localhost:8000/analizar"

# Variable para controlar el servidor
servidor_proceso = None

def iniciar_servidor():
    """Inicia el servidor FastAPI en segundo plano"""
    global servidor_proceso
    
    try:
        # Verificar si el puerto 8000 ya está en uso
        response = requests.get("http://localhost:8000/", timeout=2)
        if response.status_code == 200:
            print("Servidor ya está corriendo")
            return True
    except:
        pass
    
    try:
        # Iniciar el servidor
        servidor_proceso = subprocess.Popen(
            ["python", "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # Esperar a que el servidor esté listo
        for _ in range(10):  # Intentar por 10 segundos
            try:
                time.sleep(1)
                response = requests.get("http://localhost:8000/", timeout=2)
                if response.status_code == 200:
                    print("Servidor iniciado correctamente")
                    return True
            except:
                continue
        
        messagebox.showerror("Error", "No se pudo iniciar el servidor")
        return False
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar servidor:\n{e}")
        return False

def detener_servidor():
    """Detiene el servidor FastAPI"""
    global servidor_proceso
    if servidor_proceso:
        servidor_proceso.terminate()
        servidor_proceso = None
        print("Servidor detenido")

def enviar_reseña():
    id_cliente = entry_id.get().strip()
    reseña = text_reseña.get("1.0", tk.END).strip()

    if not id_cliente or not reseña:
        messagebox.showwarning("Error", "Debes llenar todos los campos.")
        return
    
    # Validar que ID sea numérico
    try:
        int(id_cliente)
    except ValueError:
        messagebox.showwarning("Error", "El ID del cliente debe ser un número.")
        return

    try:
        # Mostrar indicador de carga
        resultado_label.config(text="Analizando...", fg="blue")
        root.update()
        
        response = requests.post(
            API_URL,
            json={
                "id_cliente": int(id_cliente),
                "reseña": reseña
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            resultado_label.config(
                text=f"✅ Sentimiento: {data['resultado']}\n⭐ Estrellas: {data['estrellas']}",
                fg="green"
            )
            # Limpiar campos después de enviar
            text_reseña.delete("1.0", tk.END)
        else:
            resultado_label.config(
                text=f"Error del servidor: {response.status_code}",
                fg="red"
            )

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "No se puede conectar al servidor. Verifica que esté corriendo.")
        resultado_label.config(text="❌ Servidor no disponible", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}")
        resultado_label.config(text="❌ Error en el análisis", fg="red")

def cerrar_aplicacion():
    """Función para cerrar la aplicación correctamente"""
    detener_servidor()
    root.destroy()

# ------------------- Tkinter UI --------------------
root = tk.Tk()
root.title("Clasificador de Reseñas – Escritorio")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

# Estilos
titulo_font = ("Arial", 16, "bold")
label_font = ("Arial", 11)
entry_font = ("Arial", 10)
button_font = ("Arial", 11, "bold")

# Título
tk.Label(
    root, 
    text="📝 Clasificador de Reseñas", 
    font=titulo_font, 
    bg="#f0f0f0"
).pack(pady=15)

# Marco para formulario
frame_form = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
frame_form.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# ID del cliente
tk.Label(
    frame_form, 
    text="ID Cliente:", 
    font=label_font, 
    bg="#ffffff"
).pack(anchor="w", padx=10, pady=(10, 5))

entry_id = tk.Entry(frame_form, font=entry_font, width=40)
entry_id.pack(padx=10, pady=(0, 10))

# Reseña
tk.Label(
    frame_form, 
    text="Escribe la reseña:", 
    font=label_font, 
    bg="#ffffff"
).pack(anchor="w", padx=10, pady=(0, 5))

text_reseña = tk.Text(frame_form, height=8, width=45, font=entry_font)
text_reseña.pack(padx=10, pady=(0, 10))

# Botón de enviar
btn_frame = tk.Frame(frame_form, bg="#ffffff")
btn_frame.pack(pady=10)

btn_enviar = tk.Button(
    btn_frame,
    text="🚀 Analizar Reseña",
    font=button_font,
    command=enviar_reseña,
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10
)
btn_enviar.pack()

# Resultado
resultado_label = tk.Label(
    root, 
    text="Esperando análisis...", 
    font=("Arial", 12),
    bg="#f0f0f0",
    justify=tk.LEFT
)
resultado_label.pack(pady=20)

# Estado del servidor
estado_servidor = tk.Label(
    root,
    text="⚙️ Iniciando servidor...",
    font=("Arial", 9),
    bg="#f0f0f0",
    fg="blue"
)
estado_servidor.pack()

# Iniciar servidor al abrir la aplicación
def iniciar_servidor_background():
    if iniciar_servidor():
        estado_servidor.config(text="✅ Servidor conectado", fg="green")
    else:
        estado_servidor.config(text="❌ Servidor no disponible", fg="red")

# Usar thread para no bloquear la interfaz
threading.Thread(target=iniciar_servidor_background, daemon=True).start()

# Configurar cierre de ventana
root.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

# Centrar ventana
root.eval('tk::PlaceWindow . center')

root.mainloop()
import subprocess
import sys
import threading
import time

def ejecutar_servidor():
    """Ejecuta el servidor FastAPI"""
    subprocess.run([sys.executable, "main.py"])

def ejecutar_interfaz():
    """Ejecuta la interfaz de escritorio"""
    time.sleep(3)  # Esperar que el servidor inicie
    subprocess.run([sys.executable, "app_desktop.py"])

if __name__ == "__main__":
    print("Iniciando aplicación completa...")
    
    # Crear hilos para ejecutar ambos procesos
    servidor_thread = threading.Thread(target=ejecutar_servidor)
    interfaz_thread = threading.Thread(target=ejecutar_interfaz)
    
    servidor_thread.start()
    interfaz_thread.start()
    
    servidor_thread.join()
    interfaz_thread.join()
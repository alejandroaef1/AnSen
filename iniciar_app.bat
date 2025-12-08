@echo off
echo *******************************************
echo *   CLASIFICADOR DE RESEÑAS - INICIANDO   *
echo *******************************************
echo.

echo Paso 1: Iniciando servidor de backend...
start cmd /k "title SERVIDOR & python main.py"

echo Paso 2: Esperando 7 segundos para que el servidor se inicie...
timeout /t 7 /nobreak

echo Paso 3: Iniciando aplicación de escritorio...
echo.
echo *******************************************
echo *   ¡APLICACIÓN INICIADA CORRECTAMENTE!   *
echo *******************************************
echo.
echo IMPORTANTE:
echo - No cierres la ventana del servidor (azul)
echo - Usa la ventana de la aplicación (gris) para trabajar
echo - Para salir: cierra primero la aplicación, luego el servidor
echo.

python app_desktop.py

echo.
echo *******************************************
echo *     APLICACIÓN CERRADA - INSTRUCCIONES  *
echo *******************************************
echo Para cerrar completamente:
echo 1. Ve a la ventana del servidor (título: SERVIDOR)
echo 2. Presiona CTRL+C
echo 3. Luego escribe: exit
echo.
pause
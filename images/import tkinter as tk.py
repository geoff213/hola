import tkinter as tk
from tkinter import messagebox
import RPi.GPIO as GPIO

# Configuración de los pines
relePuerta1Pin = 3
relePuerta2Pin = 4
luzPin = 5

# Inicialización de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(relePuerta1Pin, GPIO.OUT)
GPIO.setup(relePuerta2Pin, GPIO.OUT)
GPIO.setup(luzPin, GPIO.OUT)

# Estado de las puertas y la luz
puerta1Abierta = False
puerta2Abierta = False

# Funciones de control
def abrir_puerta1():
    global puerta1Abierta
    if not puerta1Abierta and not puerta2Abierta:
        GPIO.output(relePuerta1Pin, GPIO.HIGH)
        GPIO.output(luzPin, GPIO.HIGH)
        puerta1Abierta = True
        update_status()
    else:
        messagebox.showwarning("Advertencia", "No se puede abrir la puerta 1 mientras la puerta 2 está abierta.")

def cerrar_puerta1():
    global puerta1Abierta
    if puerta1Abierta:
        GPIO.output(relePuerta1Pin, GPIO.LOW)
        GPIO.output(luzPin, GPIO.LOW)
        puerta1Abierta = False
        update_status()

def update_status():
    status_text.set(f"Puerta 1: {'Abierta' if puerta1Abierta else 'Cerrada'}\nPuerta 2: {'Abierta' if puerta2Abierta else 'Cerrada'}\nLuz: {'Encendida' if puerta1Abierta else 'Apagada'}")

# Crear la ventana principal
root = tk.Tk()
root.title("Control de Puertas y Luz")

# Texto de estado
status_text = tk.StringVar()
status_label = tk.Label(root, textvariable=status_text, font=('Helvetica', 14))
status_label.pack(pady=10)

# Botones de control
abrir_puerta1_button = tk.Button(root, text="Abrir Puerta 1", command=abrir_puerta1, width=20, height=2)
abrir_puerta1_button.pack(pady=5)

cerrar_puerta1_button = tk.Button(root, text="Cerrar Puerta 1", command=cerrar_puerta1, width=20, height=2)
cerrar_puerta1_button.pack(pady=5)

# Inicializar el estado
update_status()

# Ejecutar la aplicación
root.mainloop()

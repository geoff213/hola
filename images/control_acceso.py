from flask import Flask, request, jsonify
import requests
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Configuración de las puertas y sus IPs
doors = {
    'door1': {'ip': '192.168.1.2', 'status': 'closed'},
    'door2': {'ip': '192.168.1.3', 'status': 'closed'},
}

# Configuración de los pines de los botones físicos (ejemplo para Raspberry Pi)
button_pins = {
    'button_door1': 17,  # GPIO17 para el botón de la puerta 1
    'button_door2': 18,  # GPIO18 para el botón de la puerta 2
}

# Configuración de GPIO para botones físicos
GPIO.setmode(GPIO.BCM)
for pin in button_pins.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Función para manejar la apertura de puertas mediante botones físicos
def button_callback(channel):
    for door, pin in button_pins.items():
        if channel == pin:
            open_door(door)

# Configuración de callbacks para los botones físicos
for door, pin in button_pins.items():
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

# Rutas HTTP para control de puertas

@app.route('/status', methods=['GET'])
def status():
    for door, info in doors.items():
        try:
            response = requests.get(f"http://{info['ip']}/status")
            info['status'] = response.json().get('status', 'unknown')
        except requests.RequestException:
            info['status'] = 'unknown'
    return jsonify(doors)

@app.route('/open/<door_id>', methods=['POST'])
def open_door(door_id):
    if door_id in doors:
        try:
            response = requests.post(f"http://{doors[door_id]['ip']}/open")
            if response.status_code == 200:
                doors[door_id]['status'] = 'open'
                return jsonify({'status': 'success', 'door': door_id}), 200
            else:
                return jsonify({'status': 'error', 'message': 'Failed to open door'}), response.status_code
        except requests.RequestException:
            return jsonify({'status': 'error', 'message': 'Could not reach the door'}), 500
    return jsonify({'status': 'error', 'message': 'Door not found'}), 404

@app.route('/close/<door_id>', methods=['POST'])
def close_door(door_id):
    if door_id in doors:
        try:
            response = requests.post(f"http://{doors[door_id]['ip']}/close")
            if response.status_code == 200:
                doors[door_id]['status'] = 'closed'
                return jsonify({'status': 'success', 'door': door_id}), 200
            else:
                return jsonify({'status': 'error', 'message': 'Failed to close door'}), response.status_code
        except requests.RequestException:
            return jsonify({'status': 'error', 'message': 'Could not reach the door'}), 500
    return jsonify({'status': 'error', 'message': 'Door not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

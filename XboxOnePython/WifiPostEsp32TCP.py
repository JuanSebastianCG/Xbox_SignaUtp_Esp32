import requests

# Dirección IP y puerto del ESP32
#esp32_ip = "192.168.20.72"
esp32_ip = "192.168.154.89"
esp32_ip = "192.168.106.169"
esp32_port = 80


def send_data_to_esp32(data_input):

    data_to_send = {
        "key": data_input[0],
        "value": data_input[1] 
                    }
    try:
        response = requests.post(f'http://{esp32_ip}:{esp32_port}', data=data_to_send)
        if response.status_code == 200:
            print("Datos enviados correctamente: " + esp32_ip)
        else:
            print("Error en la solicitud HTTP")
    except requests.exceptions.ConnectionError:
        print("Error de conexión")



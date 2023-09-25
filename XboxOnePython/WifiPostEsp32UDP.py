import socket

# Dirección IP y puerto del ESP32
esp32_ip = "192.168.20.72"
esp32_port = 12345  

""" def send_data_to_esp32(data_input):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            data_to_send = ",".join(str(value) for value in data_input)
            udp_socket.sendto(data_to_send.encode(), (esp32_ip, esp32_port))
            print ("Datos enviados correctamente: " + data_to_send)
    except Exception as e:
        print(f"Error al enviar datos UDP: {e}") """


def send_data_to_esp32(data_input):
    data_to_send = f"{data_input[0]}={data_input[1]}"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.sendto(data_to_send.encode(), (esp32_ip, esp32_port))
        print("Datos enviados correctamente: " + str(data_input))
    except Exception as e:
        print(f"Error al enviar datos UDP: {e}")

# Otros métodos y definiciones según sea necesario

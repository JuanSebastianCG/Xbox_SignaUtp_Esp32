import socket
import struct

# Dirección IP y puerto del ESP32
#esp32_ip = "192.168.20.72"
esp32_ip = "192.168.204.89"
esp32_port = 80 

def send_data_to_esp32(key, value):
    try:
        data_to_send = struct.pack('!Bh', key, value)  # Empaqueta el primer valor como uint8 y el segundo como int16
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.sendto(data_to_send, (esp32_ip, esp32_port))
            print("Datos: Key={}, Value={}".format(key, value), data_to_send)
    except Exception as e:
        print("Error al enviar datos UDP: {}".format(e))

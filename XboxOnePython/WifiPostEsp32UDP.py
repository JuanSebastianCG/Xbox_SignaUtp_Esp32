import socket
import struct

# Dirección IP y puerto del ESP32
#esp32_ip = "192.168.204.89"
esp32_ip = "192.168.20.72"
esp32_port = 80

def send_data_to_esp32(data):
    try:
        key, values = data
        value1, value2 = values
        # Empaqueta key como uint8, value1 y value2 como int16 cada uno
        data_to_send = struct.pack('!Bhh', key, value1, value2)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.sendto(data_to_send, (esp32_ip, esp32_port))
            print("Datos: Key={}, Value1={}, Value2={}".format(key, value1, value2), data_to_send)
    except Exception as e:
        print("Error al enviar datos UDP: {}".format(e))

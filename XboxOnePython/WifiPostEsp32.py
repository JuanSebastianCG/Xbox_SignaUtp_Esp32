import aiohttp
import asyncio

# Dirección IP y puerto del ESP32
esp32_ip = "192.168.20.72"
esp32_port = 80

# Crear una instancia de sesión fuera de la función
session = aiohttp.ClientSession()

async def send_data_to_esp32(data_Input):
    print("Enviando " + str(data_Input) + " al ESP32")
    url = f"http://{esp32_ip}:{esp32_port}"
    try:
        # Realiza la solicitud POST sin esperar la respuesta
        await session.post(url, json=data_Input)
    except Exception as e:
        print(f"Error al enviar solicitud POST al ESP32: {str(e)}")

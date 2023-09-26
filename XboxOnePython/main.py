import XboxInputController as xic
import WifiPostEsp32UDP as wpeUDP
import threading
import queue

# Número máximo de hilos permitidos
max_threads = 15

# Cola para encolar los datos a enviar al ESP32
data_queue = queue.Queue(max_threads)

def send_data_Server():
    while True:
        input = data_queue.get()
        if input is not None:
            wpeUDP.send_data_to_esp32(input[0], input[1])
        data_queue.task_done()


def XboxInputController(device):
    # Inicia el hilo para enviar datos
    send_data_thread = threading.Thread(target=send_data_Server)
    send_data_thread.start()

    for event in device.read_loop():
        input = xic.controllerListener(event)
        if input is not None:
            try:
                data_queue.put(input, block=False)
            except queue.Full:
                print("Cola de datos llena, espera para enviar más datos")

def main():
    
    device = xic.findBluetoothController()
    XboxInputController(device)
   

if __name__ == "__main__":
    main()

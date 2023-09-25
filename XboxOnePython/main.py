from evdev import ecodes
import XboxInputController as xic
import WifiPostEsp32 as wpe

def XboxInputController(device):
    for event in device.read_loop():
        input = xic.controllerListener(event)
        if input is not None:
            wpe.send_data_to_esp32(input)

def main():
    try:
        device = xic.findBluetoothControll()
        XboxInputController(device)
    except Exception as e:
        print(f"Error en la lectura del control de Xbox: {e}")

if __name__ == "__main__":
    main()

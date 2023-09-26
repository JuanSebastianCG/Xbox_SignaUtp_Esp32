import evdev
from evdev import ecodes
import numpy as np




CENTER_TOLERANCE = 500
STICK_MAX = 65536

STIK_MAX_SIMULATED = STICK_MAX/2


# Define los rangos para los ejes analógicos
newLimits = {
    15: (-STIK_MAX_SIMULATED,STIK_MAX_SIMULATED),
    16: (-STIK_MAX_SIMULATED,STIK_MAX_SIMULATED),
    17: (-STIK_MAX_SIMULATED,STIK_MAX_SIMULATED),
    18: (-STIK_MAX_SIMULATED,STIK_MAX_SIMULATED),
    19: (0, 2000),
    20: (0, 2000),
}

# Rangos por defecto
defaultLimits = {
    15: (0, 65000),
    16: (0, 65000),
    17: (0, 65000),
    18: (0, 65000),
    19: (0, 1023),
    20: (0, 1023),
}

event_mappings = {
    ecodes.BTN_SOUTH: 1,
    ecodes.BTN_NORTH: 2,
    ecodes.BTN_WEST: 3,
    ecodes.BTN_EAST: 4, 
    #ecodes.ABS_HAT0Y: {5: -1, 6: 1},
    #ecodes.ABS_HAT0X: {7: -1, 8: 1},
    ecodes.BTN_TL: 11, # gatillo izquierdo SUPERIOR
    ecodes.BTN_TR: 12, # gatillo derecho SUPERIOR
    ecodes.BTN_START: 13, # botón START
    ecodes.BTN_SELECT: 14, # botón SELECT
    ecodes.ABS_Z: {15: ()}, # joystick izquierdo arriba-abajo
    ecodes.ABS_RZ: {16: ()}, # joystick izquierdo izquierda-derecha
    ecodes.ABS_X: {17: ()}, # joystick derecho arriba-abajo
    ecodes.ABS_Y: {18: ()}, # joystick derecho izquierda-derecha
    ecodes.ABS_GAS: {19: ()}, # gatillo izquierdo
    ecodes.ABS_BRAKE: {20: ()} # gatillo derecho
}


def findBluetoothController():
    """Encuentra el dispositivo de entrada del control de Xbox."""
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

    for device in devices:
        if "Xbox" in device.name:
            return device

    return None


def controllerListener(event):
    if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
        input_data = None
        if event.type == ecodes.EV_KEY:
            if event.value == 1:  # Solo cuando se presionan los botones
                input_data = [event_mappings.get(event.code), 1]

        # si el evento es un evento absoluto y el valor no es nulo(joistick o gatillos o cruz)
        elif event.type == ecodes.EV_ABS and event.value is not None:
            print(event.value)
            input_data = event_mappings.get(event.code)
            if input_data:
                index = list(input_data.keys())[0]
                input_data = [index,event.value] 
                input_data[1] =  np.interp(event.value, defaultLimits[index], newLimits[index]).astype(int)
        print(event.value)
            
        return input_data
    return None

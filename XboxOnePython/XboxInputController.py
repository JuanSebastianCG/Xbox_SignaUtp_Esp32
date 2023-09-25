import evdev
from evdev import ecodes
import numpy as np

def findBluetoothController():
    """Encuentra el dispositivo de entrada del control de Xbox."""
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

    for device in devices:
        if "Xbox" in device.name:
            return device

    return None

# Define los rangos para los ejes analógicos
newLimits = {
    15: (0, 2000),
    16: (0, 2000),
    17: (0, 2000),
    18: (0, 2000),
    19: (0, 255),
    20: (0, 255),
}

# Rangos por defecto
defaultLimits = {
    15: (0, 65000),
    16: (0, 65000),
    17: (0, 65000),
    18: (0, 65000),
    19: (0, 255),
    20: (0, 255),
}

event_mappings = {
    ecodes.BTN_NORTH: 1,
    ecodes.BTN_SOUTH: 2,
    ecodes.BTN_WEST: 3,
    ecodes.BTN_EAST: 4,
    ecodes.ABS_HAT0Y: {5: 1, 6: -1},
    ecodes.ABS_HAT0X: {7: 1, 8: -1},
    ecodes.BTN_TL: 11,
    ecodes.BTN_TR: 12,
    ecodes.BTN_START: 13,
    ecodes.BTN_SELECT: 14,
    ecodes.ABS_Z: {15: ()},
    ecodes.ABS_RZ: {16: ()},
    ecodes.ABS_X: {17: ()},
    ecodes.ABS_Y: {18: ()},
    ecodes.ABS_GAS: {19: ()},
    ecodes.ABS_BRAKE: {20: ()}
}
def controllerListener(event):
    if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
        input_data = None
        if event.type == ecodes.EV_KEY:
            if event.value == 1:  # Solo cuando se presionan los botones
                input_data = [event_mappings.get(event.code), 1]
                
        elif event.type == ecodes.EV_ABS and event.value is not None:
            input_data = event_mappings.get(event.code)
            if input_data:
                index = list(input_data.keys())[0]
                input_data = [index,event.value] 
                if newLimits.get(index):
                    input_data[1] = np.interp(event.value, defaultLimits[index], newLimits[index])
                elif event.value == 0 :
                    input_data = None
                    
        return input_data
    return None

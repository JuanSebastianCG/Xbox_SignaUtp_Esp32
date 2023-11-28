import evdev
from evdev import list_devices, InputDevice, ecodes
import numpy as np

CENTER_TOLERANCE = 2000
STICK_MAX = 65536
STICK_OUTPUT= STICK_MAX/2-500

event_mappings = {
    ecodes.BTN_SOUTH: 1,
    ecodes.BTN_NORTH: 2,
    ecodes.BTN_WEST: 3,
    ecodes.BTN_EAST: 4,
    ecodes.BTN_TL: 11,
    ecodes.BTN_TR: 12,
    ecodes.BTN_START: 13,
    ecodes.BTN_SELECT: 14,
    ecodes.ABS_Z: 15,
    ecodes.ABS_RZ: 16,
    ecodes.ABS_X: 17,
    ecodes.ABS_Y: 18,
    ecodes.ABS_GAS: 19,
    ecodes.ABS_BRAKE: 20
}
center = {axis: STICK_OUTPUT for axis in [17, 18, 15, 16]}
last = center.copy()

# Encuentra el dispositivo de entrada del control de Xbox
def findBluetoothController():
    device = None
    while device is None:
        try:
            for fn in list_devices():
                device = InputDevice(fn)
                if "Xbox" in device.name:
                    print("Control de Xbox encontrado")
                    break
        except OSError:
            print("No se encontró el control de Xbox, intentando de nuevo...")
    return device

# Normaliza un valor del eje
def normalize_axis(axis_value):
    return (axis_value - STICK_OUTPUT) / (STICK_OUTPUT)

# Convierte coordenadas cartesianas a polares
def polarCoordinates(x, y):
    r = np.sqrt(x**2 + y**2)
    r = int(np.interp(r, (0, 1), (0, 100)))
    theta = np.arctan2(y, x)
    theta = int(np.rad2deg(theta))
    # Asegurarse de que el ángulo esté en el rango de 0 a 360 grados
    theta = (-theta + 90 ) % 360
    return r, theta


# Escuchar los eventos del control de Xbox
def controllerListener(event):
    if event.type in [ecodes.EV_KEY, ecodes.EV_ABS]:
        input_data = None
        if event.value == 1:
            input_data = [event_mappings.get(event.code), (0,0)]
        elif event.type == ecodes.EV_ABS and event.value is not None:
            axis = event_mappings.get(event.code)
            if axis is not None:
                last[axis] = event.value
                if axis in [15, 16, 17, 18]:
                    x = normalize_axis(last[15]) if axis in [15, 16] else normalize_axis(last[17])
                    y = normalize_axis(last[16]) * -1 if axis in [15, 16] else normalize_axis(last[18]) * -1
                    x = 0 if abs(x) <= CENTER_TOLERANCE / (STICK_OUTPUT) else x
                    y = 0 if abs(y) <= CENTER_TOLERANCE / (STICK_OUTPUT) else y
                    input_data = [axis, (int(np.interp(x, (-1, 1), (-STICK_OUTPUT, STICK_OUTPUT))), int(np.interp(y, (-1, 1), (-STICK_OUTPUT, STICK_OUTPUT))))]
                    #polar = polarCoordinates(x, y)
                    #input_data = [axis,(polar[0],polar[1])]
                elif axis in [19, 20]:
                    input_data = [axis, (event.value,0)]
        return input_data




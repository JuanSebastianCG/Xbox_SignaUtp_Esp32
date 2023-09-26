import evdev
from evdev import list_devices, InputDevice, categorize, ecodes

CENTER_TOLERANCE = 2000
STICK_MAX = 65536

def findBluetoothController():
    """Encuentra el dispositivo de entrada del control de Xbox."""
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    return next((device for device in devices if "Xbox" in device.name), None)

dev = findBluetoothController()

event_mappings = {
    ecodes.BTN_SOUTH: 1,
    ecodes.BTN_NORTH: 2,
    ecodes.BTN_WEST: 3,
    ecodes.BTN_EAST: 4,
    ecodes.BTN_TL: 11,
    ecodes.BTN_TR: 12,
    ecodes.BTN_START: 13,
    ecodes.BTN_SELECT: 14,
    ecodes.ABS_Z: 'rs_x',
    ecodes.ABS_RZ: 'rs_y',
    ecodes.ABS_X: 'ls_x',
    ecodes.ABS_Y: 'ls_y',
    ecodes.ABS_GAS: {19: ()},
    ecodes.ABS_BRAKE: {20: ()}
}

center = {axis: STICK_MAX / 2 for axis in ['ls_x', 'ls_y', 'rs_x', 'rs_y']}
last = center.copy()

def calibrate():
    center.update(last)
    print('calibrated')

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY and categorize(event).keycode[0] == "BTN_WEST":
        calibrate()
    elif event.type == ecodes.EV_ABS and event.code in event_mappings:
        axis = event_mappings[event.code]
        last[axis] = event.value

        if axis in ['rs_x', 'rs_y']:
            x = (last['rs_x'] - center['rs_x']) / (STICK_MAX / 2)
            y = (last['rs_y'] - center['rs_y']) / (STICK_MAX / 2) * -1
        elif axis in ['ls_x', 'ls_y']:
            x = (last['ls_x'] - center['ls_x']) / (STICK_MAX / 2)
            y = (last['ls_y'] - center['ls_y']) / (STICK_MAX / 2) * -1
        else:
            continue

        x = 0 if abs(x) <= CENTER_TOLERANCE / (STICK_MAX / 2) else x
        y = 0 if abs(y) <= CENTER_TOLERANCE / (STICK_MAX / 2) else y

        print(f'X: {x}, Y: {y}')

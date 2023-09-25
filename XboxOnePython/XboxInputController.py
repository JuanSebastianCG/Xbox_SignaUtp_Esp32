import evdev
from evdev import ecodes

""" encontrar el dispositivo de entrada del control de Xbox """
def findBluetoothControll():
    """Encuentra el dispositivo de entrada del control de Xbox."""
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

    for device in devices:
        if "Xbox" in device.name:
            return device

    return None


""" tipos de entradas del control de Xbox """
def findButtonXYAB(event):
    if event.type == ecodes.EV_KEY:
        if event.code == ecodes.BTN_NORTH and event.value == 1:
            return ["Y", event.value]
        elif event.code == ecodes.BTN_SOUTH and event.value == 1:
            return ["A", event.value]
        elif event.code == ecodes.BTN_WEST and event.value == 1:
            return ["X", event.value]
        elif event.code == ecodes.BTN_EAST and event.value == 1:
            return ["B", event.value]
        else:
            return None
        
def findButtonDPAD(event):
    if event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_HAT0Y:
            if event.value == 1:
                return ["DPAD_DOWN", 4]
            elif event.value == -1:
                return ["DPAD_UP", 6]
            else:
                return None
        elif event.code == ecodes.ABS_HAT0X:
            if event.value == 1:
                return ["DPAD_RIGHT", 7]
            elif event.value == -1:
                return ["DPAD_LEFT", 5]
            else:
                return None

def findButtonLTRT(event):
    if event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_BRAKE:
            return ["LT", event.value]
        elif event.code == ecodes.ABS_GAS:
            return ["RT", event.value]
        else:
            return None
            
def findButtonLBRB(event):
    if event.type == ecodes.EV_KEY:
        if event.code == ecodes.BTN_TL and event.value == 1:
            return ["LB", event.value]
        elif event.code == ecodes.BTN_TR and event.value == 1:
            return ["RB", event.value]
        else:
            return None
        
def findButtonStartBack(event):
    if event.type == ecodes.EV_KEY:
        if event.code == ecodes.BTN_START and event.value == 1:
            return ["START", event.value]
        elif event.code == ecodes.BTN_SELECT and event.value == 1:
            return ["BACK", event.value]
        else:
            return None
        
def findRightJoystick(event):
    if event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_Z:
            return ["RIGHT_JRD", event.value]
        elif event.code == ecodes.ABS_RZ:
            return ["RIGHT_JLR", event.value]
        else:
            return None
def findLeftJoystick(event):
    if event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_X:
            return ["LEFT_JRD", event.value]
        elif event.code == ecodes.ABS_Y:
            return ["LEFT_JLF", event.value]
        else:
            return None
        

def controllerListener(event):
        aux = findButtonXYAB(event)
        if aux != None:
            #print(aux)
            return aux
        aux = findButtonDPAD(event)
        if aux != None:
            #print(aux)
            return aux
        aux = findButtonLTRT(event)
        if aux != None:
            #print(aux)
            return aux
        aux = findButtonLBRB(event)
        if aux != None:
            #print(aux)
            return aux
        aux = findButtonStartBack(event)
        if aux != None:
            #print(aux)
            return aux
        aux = findRightJoystick(event)
        if aux != None:
            #print(aux)
            return aux
        aux = findLeftJoystick(event)
        if aux != None:
            #print(aux)
            return aux
        
        return None

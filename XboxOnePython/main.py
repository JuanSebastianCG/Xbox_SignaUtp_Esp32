from evdev import ecodes
import asyncio

import XboxInputController as xic
import WifiPostEsp32 as wpe  

async def XboxInputController(device):
    for event in device.read_loop():
        input = xic.controllerListener(event)
        if input is not None:
            await wpe.send_data_to_esp32(input)

def main():
    device = xic.findBluetoothControll()
    # loop is a global variable that is used to run the event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(XboxInputController(device))
    finally:
        loop.run_until_complete(wpe.close_session())
    
if __name__ == "__main__":
    main()

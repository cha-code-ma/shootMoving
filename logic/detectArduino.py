"""
Github: cha-code-ma
In this file, logic will be made of
connecting to arduino.

"""
import argparse
import asyncio


from bleak import BleakClient
from bleak import BleakScanner

ARDUINO_LOCAL_NAME = "Chakir"

#led
LED_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
on_value = bytearray([0x01])
off_value = bytearray([0x00])

async def find_ble_device(args: argparse.Namespace):
    print("scanning")

    devices = await BleakScanner.discover(
        return_adv=True, cb=dict(use_bdaddr=args.macos_use_bdaddr)
    )

    for d, a in devices.values():
        if d.name == ARDUINO_LOCAL_NAME:
            print("Arduino found")
            print(d.address, d.name)
            return d, a

    return None, None
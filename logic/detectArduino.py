"""
Github: cha-code-ma
In this file, logic will be made of
connecting to arduino.

"""
import argparse
import asyncio
import struct # to decode
from PyQt5.QtCore import QThread, pyqtSignal
from bleak import BleakClient
from bleak import BleakScanner

ARDUINO_LOCAL_NAME = "Chakir"

#led
LED_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
SENSOR_UUID = "4664E7A1-5A13-BFFF-4636-7D0A4B16496C"
on_value = bytearray([0x01])
off_value = bytearray([0x00])

class BleCommunicationManager(QThread):
    statusUpdate = pyqtSignal(bool)
    data = pyqtSignal(dict)

    def run(self):
        asyncio.run(self._main())

    async def find_ble_device(self, args: argparse.Namespace):
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


    async def runmain(self, d, a):
        async with BleakClient(d.address) as client:
            print("Connected")

            for i in range(10):
                print("LED on")
                await client.write_gatt_char(LED_UUID, on_value)
                await asyncio.sleep(1)

                print("LED off")
                await client.write_gatt_char(LED_UUID, off_value)
                await asyncio.sleep(1)

            print("Done")

    async def _main(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--macos-use-bdaddr",
            action="store_true",
            help="when true use Bluetooth address instead of UUID on macOS",
        )


        args = parser.parse_args()
        (d,a) = asyncio.run(self.find_ble_device(args))
        if (d,a) != (None, None):
            asyncio.run(self.runmain(d,a))
        else:
            print("arduino not found")
        async with BleakClient(d.address) as client:
            self.statusUpdate.emit(True)

            while client.is_connected:
                data = await client.read_gatt_char(SENSOR_UUID)
                values = struct.unpack('7f', data)
                valuesDict = {'ax' : values[0], 'ay' : values[1], 'az' : values[2],
                              'gx' : values[3], 'gy' : values[4], 'gz' : values[5]
                              }
                self.data.emit(valuesDict)
                await asyncio.sleep(0.2)
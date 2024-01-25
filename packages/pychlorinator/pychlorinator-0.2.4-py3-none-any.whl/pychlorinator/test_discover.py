import asyncio
from bleak import BleakScanner

UUID_ASTRALPOOL_SERVICE = bytes.fromhex("4500000198b74e29a03f160174643001")

async def main():

    devices = await BleakScanner.discover(service_uuid=UUID_ASTRALPOOL_SERVICE)
    for device in devices:
        print(f"Device name: {device.name}, Address: {device.address}")

asyncio.run(main())

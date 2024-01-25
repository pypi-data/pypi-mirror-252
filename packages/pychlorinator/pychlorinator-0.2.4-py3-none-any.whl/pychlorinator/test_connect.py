import pychlorinator.chlorinator
import asyncio
from bleak import BleakClient

from pychlorinator.chlorinator_parsers import (
    ChlorinatorState,
)


UUID_ASTRALPOOL_SERVICE = "45000001-98b7-4e29-a03f-160174643001"
UUID_SLAVE_SESSION_KEY = "45000002-98b7-4e29-a03f-160174643001"
UUID_MASTER_AUTHENTICATION = "45000003-98b7-4e29-a03f-160174643001"
UUID_CHLORINATOR_STATE = "45000200-98b7-4e29-a03f-160174643001"

DEVICE_UUID = "8781FCA2-9586-7068-58B6-78ADA07DF377"
ACCESS_CODE = bytes("H7PB", "utf_8")


async def main():

    async with BleakClient(address_or_ble_device=DEVICE_UUID) as client:
        session_key = await client.read_gatt_char(UUID_SLAVE_SESSION_KEY)
        print(f"got session key {session_key.hex()}")

        mac = pychlorinator.chlorinator.encrypt_mac_key(session_key, ACCESS_CODE)
        print(f"mac key to write {mac.hex()}")
        await client.write_gatt_char(UUID_MASTER_AUTHENTICATION, mac)

        databytes = pychlorinator.chlorinator.decrypt_characteristic(
            await client.read_gatt_char(UUID_CHLORINATOR_STATE), session_key)
        print(f"state data {mac.hex()}")

        state = ChlorinatorState(databytes)
        print("Chlorinator state: ")
        print(vars(state))

asyncio.run(main())

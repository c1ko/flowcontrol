import asyncio
from bleak import BleakClient

ADDRESS      = "YOUR MIXER ADDRESS"
SERVICE_UUID = "14839ad4-8d7e-415c-9a42-167340cf2339"
CHAR_UUID    = "0034594a-a8e7-4b1a-a6b1-cd5243059a57"

KEEPALIVE_INTERVAL = 5
DUMMY_CHAR_UUID = "00002a00-0000-1000-8000-00805f9b34fb" 

HANDSHAKE_RESPONSE = bytes.fromhex(
    "39 01 38 3e 3a 0e 50 85 8d 7c 37 98 17 82 ce 0d 99 7f 31"
)
FINAL_ACK = bytes.fromhex("37 01 38")

def compute_checksum(hex_stream):
    byte_values = [int(b, 16) for b in hex_stream]
    checksum = sum(byte_values) & 0xFF
    return f"{checksum:02X}"

def gen_mute_channel(channel, mute=True):
    hexbytes = ["08", "01", f"{channel:02}", "01" if mute else "00"]
    hexbytes.append(compute_checksum(hexbytes))
    return hexbytes

async def run_handshake():
    # Event to fire when we see seq==1 of 0x35
    got_frag1 = asyncio.Event()

    def notification_handler(_: int, data: bytearray):
        cmd, seq = data[0], data[1]
        if cmd == 0x35 and seq == 0x01 and not got_frag1.is_set():
            print(f"Got handshake fragment1: {data.hex()}")
            got_frag1.set()
        else:
            pass

    async with BleakClient(ADDRESS, service_uuids=[SERVICE_UUID]) as client:
        print("Connected:", client.is_connected)

        await client.start_notify(CHAR_UUID, notification_handler)

        # wait until we catch that fragment1
        await got_frag1.wait()

        # send 0x39 handshake response
        print("Sending handshake response (0x39)…")
        await client.write_gatt_char(CHAR_UUID, HANDSHAKE_RESPONSE, response=True)

        # send 0x37 final ack / state‐request
        print("Sending final ack (0x37)…")
        await client.write_gatt_char(CHAR_UUID, FINAL_ACK, response=True)

        print("Handshake complete, starting main loop")

        while True:
            try:
                value = await client.read_gatt_char(DUMMY_CHAR_UUID)
                #print("Keepalive read successful:", value)
            except Exception as e:
                print("Error during keepalive:", e)

            await asyncio.sleep(KEEPALIVE_INTERVAL)

        await client.write_gatt_char(CHAR_UUID, UNMUTE_CHANNEL_2, response=True)

        await client.stop_notify(CHAR_UUID)

if __name__ == "__main__":
    asyncio.run(run_handshake())
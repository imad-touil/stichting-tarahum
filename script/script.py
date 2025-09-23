from smartcard.System import readers
from smartcard.util import toHexString
import time

def main():
    r = readers()
    if len(r) == 0:
        print("No NFC readers found")
        return

    print("Available readers:")
    for i, reader in enumerate(r):
        print(f"{i}: {reader}")

    reader = r[0]  # pick the first reader
    connection = reader.createConnection()

    print("Waiting for a card... (place card on reader)")

    last_uid = None

    while True:
        try:
            connection.connect()
            GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            response, sw1, sw2 = connection.transmit(GET_UID)

            if sw1 == 0x90 and sw2 == 0x00:
                uid = toHexString(response)
                if uid != last_uid:  # only print when new card detected
                    print(f"✅ Card detected! UID: {uid}")
                    last_uid = uid

            connection.disconnect()
            time.sleep(0.3)

        except Exception:
            # No card present → reset last UID
            last_uid = None
            time.sleep(0.3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Exiting cleanly...")

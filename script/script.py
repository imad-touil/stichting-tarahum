from smartcard.System import readers
from smartcard.util import toHexString
import time, requests

API = "http://127.0.0.1:8000/api/scan"

def main():
    try:
        r = [reader for reader in readers() if "ACR122" in str(reader)]
        if not r:
            print("No ACR122U reader found.")
            return

        print(f"Using reader: {r[0]}")
        connection = r[0].createConnection()

        last_uid = None
        while True:
            try:
                connection.connect()
                GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
                data, sw1, sw2 = connection.transmit(GET_UID)
                if sw1 == 0x90 and sw2 == 0x00:
                    uid = toHexString(data).replace(" ", "").upper()
                    if uid != last_uid:
                        print(f"Card UID: {uid}")
                        last_uid = uid
                        requests.post(API, json={"uid": uid})
                time.sleep(0.5)
            except Exception:
                last_uid = None
                time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nStopping NFC reader...")

if __name__ == "__main__":
    main()

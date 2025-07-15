from smartcard.System import readers
from smartcard.util import toHexString
import time

def main():
    r = readers()
    if len(r) == 0:
        print("No NFC readers found")
        return

    reader = r[0]
    print(f"Using reader: {reader}")

    connection = reader.createConnection()
    print("Waiting for a card... (Press Ctrl+C to exit)")
    
    while True:
        try:
            connection.connect()
            print("Card detected!")

            # Send APDU to get UID for ISO14443 cards (like MIFARE)
            GET_UID_APDU = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            response, sw1, sw2 = connection.transmit(GET_UID_APDU)

            if sw1 == 0x90 and sw2 == 0x00:
                print("Card UID:", toHexString(response))
            else:
                print(f"Failed to get UID: SW1={sw1:X}, SW2={sw2:X}")

            print("Remove card...")
            while True:
                try:
                    connection.disconnect()
                    break
                except:
                    time.sleep(0.1)

            print("Waiting for next card...\n")
            time.sleep(1)

        except Exception as e:
            time.sleep(0.5)

if __name__ == "__main__":
    main()

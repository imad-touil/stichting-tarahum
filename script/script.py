from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import NoCardException
import time

def main():
    r = readers()
    if len(r) == 0:
        print("No NFC readers found. Make sure the reader is connected and pcscd is running.")
        return

    reader = r[0]
    print(f"Using reader: {reader}")

    connection = reader.createConnection()

    print("Waiting for a card... (Press Ctrl+C to exit)")

    last_uid = None
    while True:
        try:
            # Attempt connection
            connection.connect()

            # Send APDU command to get UID
            GET_UID_APDU = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            response, sw1, sw2 = connection.transmit(GET_UID_APDU)

            if sw1 == 0x90 and sw2 == 0x00:
                uid = toHexString(response)
                if uid != last_uid:
                    print("Card detected! UID:", uid)
                    last_uid = uid
            else:
                print(f"Failed to get UID: SW1={sw1:X}, SW2={sw2:X}")

        except NoCardException:
            if last_uid is not None:
                print("Card removed. Waiting for new card...\n")
                last_uid = None

        except Exception as e:
            print("Error:", e)

        time.sleep(0.5)

if __name__ == "__main__":
    main()

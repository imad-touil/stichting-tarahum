from smartcard.System import readers
from smartcard.util import toHexString

def read_nfc():
    # Get all available readers
    reader_list = readers()
    if not reader_list:
        print("No readers available!")
        return
    
    print("Available readers:", reader_list)
    
    # Use the first reader (modify if you have multiple)
    reader = reader_list[0]
    print("Using:", reader)
    
    try:
        # Create a connection to the reader
        connection = reader.createConnection()
        connection.connect()
        
        # Get ATR (Answer To Reset)
        atr = connection.getATR()
        print("ATR:", toHexString(atr))
        
        # Send APDU commands to interact with the card
        # This is a basic command to select the MF (Master File)
        SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]
        data, sw1, sw2 = connection.transmit(SELECT)
        
        if sw1 == 0x90 and sw2 == 0x00:
            print("Card UID:", toHexString(data))
        else:
            print("Error reading card:", hex(sw1), hex(sw2))
            
    except Exception as e:
        print("Error:", e)
    finally:
        if 'connection' in locals():
            connection.disconnect()

if __name__ == "__main__":
    while True:
        print("\nWaiting for NFC card... (Ctrl+C to exit)")
        read_nfc()
        input("Press Enter to scan again...")
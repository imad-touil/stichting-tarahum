from flask import Flask, jsonify, render_template
from smartcard.System import readers
from smartcard.util import toHexString
import threading
import time

app = Flask(__name__)
latest_uid = None

def nfc_reader():
    global latest_uid
    r = readers()
    if len(r) == 0:
        print("No NFC readers found")
        return

    reader = r[0]
    connection = reader.createConnection()
    print("✅ Reader detected:", reader)
    print("Waiting for a card...")

    last_uid = None
    while True:
        try:
            # Try to connect to card
            connection.connect()
            GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            response, sw1, sw2 = connection.transmit(GET_UID)

            if sw1 == 0x90 and sw2 == 0x00:  # success
                uid = toHexString(response).replace(" ", "")
                if uid != last_uid:
                    latest_uid = uid
                    print(f"New card detected! UID: {uid}")
                    last_uid = uid

            connection.disconnect()
            time.sleep(0.3)

        except Exception:
            # No card present
            last_uid = None
            time.sleep(0.3)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_uid")
def get_uid():
    return jsonify({"uid": latest_uid})

if __name__ == "__main__":
    # run NFC reader in background
    t = threading.Thread(target=nfc_reader, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000, debug=True)

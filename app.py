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
    print("Waiting for a card... (place card on reader)")

    last_uid = None
    while True:
        try:
            connection.connect()
            GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            response, sw1, sw2 = connection.transmit(GET_UID)

            if sw1 == 0x90 and sw2 == 0x00:
                uid = toHexString(response)
                if uid != last_uid:
                    latest_uid = uid
                    print(f"✅ Card detected! UID: {uid}")
                    last_uid = uid

            connection.disconnect()
            time.sleep(0.3)

        except Exception:
            last_uid = None
            time.sleep(0.3)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_uid")
def get_uid():
    return jsonify({"uid": latest_uid})

if __name__ == "__main__":
    t = threading.Thread(target=nfc_reader, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000, debug=True)

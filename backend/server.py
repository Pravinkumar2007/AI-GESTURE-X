from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time


print("SERVER.PY LOADED")


app = Flask(__name__)

CORS(app)


# =========================================================
# GLOBAL SYSTEM STATE
# =========================================================

system_running = False
current_gesture = "WAITING"
gesture_confidence = 0

camera_status = False
ai_status = False


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return jsonify({
        "status": "AI Gesture Control Backend Running",
        "message": "Flask server is working",
        "port": 5000
    })


# =========================================================
# STATUS
# =========================================================

@app.route("/api/status")
def status():

    return jsonify({

        "system": system_running,

        "camera": camera_status,

        "ai": ai_status,

        "gesture": current_gesture,

        "confidence": gesture_confidence

    })


# =========================================================
# START SYSTEM
# =========================================================

@app.route("/api/start", methods=["POST"])
def start_system():

    global system_running
    global camera_status
    global ai_status

    system_running = True
    camera_status = True
    ai_status = True

    print("SYSTEM STARTED FROM FRONTEND")

    return jsonify({

        "success": True,

        "message": "Gesture system started",

        "system": True,

        "camera": True,

        "ai": True

    })


# =========================================================
# STOP SYSTEM
# =========================================================

@app.route("/api/stop", methods=["POST"])
def stop_system():

    global system_running
    global camera_status
    global ai_status

    system_running = False
    camera_status = False
    ai_status = False

    print("SYSTEM STOPPED FROM FRONTEND")

    return jsonify({

        "success": True,

        "message": "Gesture system stopped",

        "system": False,

        "camera": False,

        "ai": False

    })


# =========================================================
# GESTURE
# =========================================================

@app.route("/api/gesture")
def gesture():

    return jsonify({

        "gesture": current_gesture,

        "confidence": gesture_confidence

    })


# =========================================================
# SERVER
# =========================================================

if __name__ == "__main__":

    print("------------------------------------------")
    print("       AI GESTURE CONTROL SERVER")
    print("------------------------------------------")
    print()
    print("Frontend : http://127.0.0.1:5501")
    print("Backend  : http://127.0.0.1:5000")
    print()
    print("Flask server starting...")
    print("------------------------------------------")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True
    )
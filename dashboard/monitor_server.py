import os
import sys
import json
import threading
import time
from flask import Flask, jsonify, send_from_directory
from datetime import datetime, timedelta
import logging
from extract_log import extract_kuzco_results, save_to_json

# config & path
if os.path.exists('extract_log.py'):
    sys.path.append('.')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("monitoring.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__, static_folder='.')
PORT = 5050
HOST = '0.0.0.0'
JSON_FILE = 'inference_results.json'
RESET_INTERVAL = 4 * 60 * 60  # Reset 4h
last_reset = time.time()

# === MAINFUNCTION ===
def background_worker():
    """Updating Inferences JSON Data"""
    global last_reset
    while True:
        try:
            now = time.time()
            if now - last_reset >= RESET_INTERVAL:
                if os.path.exists(JSON_FILE):
                    backup = f"inference_results_{int(last_reset)}.json"
                    os.rename(JSON_FILE, backup)
                    logging.info(f"Reset: {JSON_FILE} → {backup}")
                last_reset = now

            # Cut & save data
            results = extract_kuzco_results()
            save_to_json(results, JSON_FILE)
            logging.info(f"Updated {JSON_FILE} → {len(results)} entries")
        except Exception as e:
            logging.error(f"Background error: {e}")
        
        time.sleep(10)  # Sync every 10s

# === ROUTES ===
@app.route('/')
def index():
    """Homepages Web dashboard"""
    try:
        return send_from_directory('.', 'index.html')
    except FileNotFoundError:
        logging.error("index.html not found in current directory")
        return jsonify({"error": "Index page not found"}), 404

@app.route('/inference_results.json')
def api_results():
    """Recall data JSON for inference"""
    try:
        results = extract_kuzco_results()
        response = jsonify(results)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    except Exception as e:
        logging.error(f"API error: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500

@app.route('/health')
def health():
    """Server Healty"""
    return jsonify({"status": "ok", "time": datetime.now().isoformat()})

# === MAINRUN ===
if __name__ == '__main__':
    if not os.path.exists('index.html'):
        logging.warning("index.html not found in current directory; ensure it exists for the web interface")

    worker = threading.Thread(target=background_worker, daemon=True)
    worker.start()
    
    # Detech IP server
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    logging.info(f"Dashboard Started → http://{ip_address}:{PORT}")
    logging.info(f"Access via browser at the above URL or http://localhost:{PORT} if local")

    app.run(host=HOST, port=PORT, threaded=True)
from flask import Flask, jsonify, send_from_directory
import threading
import time
import logging
import os
from datetime import datetime, timedelta
from extract_log import extract_kuzco_results

app = Flask(__name__, static_folder='.')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("monitoring.log"),
        logging.StreamHandler()
    ]
)

PORT = 5050
HOST = '0.0.0.0'
JSON_FILE = 'inference_results.json'
RESET_INTERVAL = 4 * 60 * 60  # reset every 4h
last_reset = time.time()

# === MAINFUNCTION===
def save_results():
    """Save results ekstract to JSON data"""
    results = extract_kuzco_results()
    with open(JSON_FILE, 'w') as f:
        f.write(jsonify(results).get_data(as_text=True))
    logging.info(f"Updated {JSON_FILE} → {len(results)} entries")

def background_worker():
    """Update Inferences JSON Data"""
    global last_reset
    while True:
        try:
            now = time.time()
            # Reset 4h
            if now - last_reset >= RESET_INTERVAL:
                if os.path.exists(JSON_FILE):
                    backup = f"inference_results_{int(last_reset)}.json"
                    os.rename(JSON_FILE, backup)
                    logging.info(f"Reset: {JSON_FILE} → {backup}")
                last_reset = now

            # Update data
            save_results()
        except Exception as e:
            logging.error(f"Background error: {e}")
        
        time.sleep(10)  # sync 10s

# === ROUTES ===
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/inference_results.json')
def api_results():
    try:
        results = extract_kuzco_results()
        response = jsonify(results)
        response.headers['Cache-Control'] = 'no-cache'
        return response
    except Exception as e:
        logging.error(f"API error: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500

@app.route('/health')
def health():
    return jsonify({"status": "ok", "time": datetime.now().isoformat()})

# === MAINRUN ===
if __name__ == '__main__':
    worker = threading.Thread(target=background_worker, daemon=True)
    worker.start()
    
    logging.info(f"Dashboard STARTED → http://<IP_SERVER>:{PORT}")
    logging.info(f"Access anymore → replace <IP_SERVER> w/ your IP server")
    
    app.run(host=HOST, port=PORT, threaded=True)

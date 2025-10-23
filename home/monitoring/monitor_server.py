import http.server
import socketserver
import os
import threading
import time
import logging
from extract_log import extract_kuzco_results, save_to_json

logging.basicConfig(
    filename='/app/monitoring/monitoring.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PORT = 5050
DIR = "/app/monitoring"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_GET(self):
        if self.path == '/inference_results.json':
            try:
                results = extract_kuzco_results()
                save_to_json(results)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                with open('/app/monitoring/inference_results.json', 'rb') as f:
                    self.wfile.write(f.read())
                logging.info("Served inference_results.json")
            except Exception as e:
                logging.error(f"Error serving inference_results.json: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Error generating results')
        else:
            super().do_GET()

def run_server():
    os.chdir(DIR)
    server_address = ('0.0.0.0', PORT)
    httpd = socketserver.TCPServer(server_address, CustomHandler)
    logging.info(f"Starting monitoring server on http://localhost:{PORT}")
    httpd.serve_forever()

def run_extractor():
    while True:
        try:
            results = extract_kuzco_results()
            save_to_json(results)
            logging.info(f"Extracted {len(results)} inference results to inference_results.json")
        except Exception as e:
            logging.error(f"Error in periodic extraction: {e}")
        time.sleep(10)  # Update every 10s

if __name__ == "__main__":
    extractor_thread = threading.Thread(target=run_extractor, daemon=True)
    extractor_thread.start()
    run_server()

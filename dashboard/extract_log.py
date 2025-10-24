import re
import json
import subprocess
import time

def get_docker_logs():
    """Ambil log real-time dari docker logs"""
    try:
        result = subprocess.run(
            ['docker', 'logs', 'kuzco-inference', '--tail', '500'],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def extract_kuzco_results():
    logs = get_docker_logs()
    results = []
    lines = [line.strip() for line in logs.split('\n') if line.strip()]

    for line in lines:
        # Filter hanya 9 pesan relevan
        if not any(msg in line for msg in [
            'Processing message', 'Sending lock message', 'Downloading generation request',
            'Received lock response', 'Successfully downloaded generation request',
            'Starting streaming inference', 'Starting inference request',
            'SUCCESS: Streaming inference completed', 'Skipping logprobs'
        ]):
            continue

        # Extract timestamp
        time_match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)', line)
        timestamp = time_match.group(1) if time_match else "Unknown"

        # Extract inbox (bagian depan saja)
        inbox_match = re.search(r'inbox: (dispatcher\.[a-zA-Z0-9]+)', line)
        inbox_id = inbox_match.group(1) if inbox_match else "N/A"

        # Tentukan status, pesan, dan action
        if 'SUCCESS: Streaming inference completed' in line:
            status = 'Completed'
            message = 'SUCCESS: Streaming inference completed'
            action = 'Inference'
        elif 'Skipping logprobs' in line:
            status = 'Completed'
            message = 'Skipping logprobs'
            action = 'Inference'
        elif 'Sending lock message' in line:
            status = 'Processing'
            message = 'Sending lock message'
            action = 'Lock'
        elif 'Received lock response' in line:
            status = 'Processing'
            message = 'Received lock response'
            action = 'Lock'
        elif 'Downloading generation request' in line:
            status = 'Processing'
            message = 'Downloading generation request'
            action = 'Download'
        elif 'Successfully downloaded generation request' in line:
            status = 'Processing'
            message = 'Successfully downloaded generation request'
            action = 'Download'
        elif 'Starting streaming inference' in line:
            status = 'Processing'
            message = 'Starting streaming inference'
            action = 'Inference'
        elif 'Starting inference request' in line:
            status = 'Processing'
            message = 'Starting inference request'
            action = 'Inference'
        else:  # Processing message
            status = 'Processing'
            message = 'Processing message'
            action = 'Processing'

        # Format date untuk Grid 2
        try:
            dt = timestamp.split("T")[0] + " " + timestamp.split("T")[1].split(".")[0]
        except:
            dt = "N/A"

        results.append({
            "date": dt,
            "model": "llama-3.2-3b-instruct-promo",
            "input_tokens": "N/A",
            "output_tokens": "N/A",
            "cost": "N/A",
            "endpoint": "/v1/chat/completions",
            "status": status,
            "inbox": inbox_id,
            "timestamp": timestamp,
            "message": message,
            "action": action
        })

    # Sortir berdasarkan timestamp (terbaru di atas)
    results.sort(key=lambda x: x['timestamp'] if x['timestamp'] != "Unknown" else "", reverse=True)

    # Batasi 50 baris
    results = results[:50]

    # Fallback jika kosong
    if not results:
        now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        results.append({
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "model": "llama-3.2-3b-instruct-promo",
            "input_tokens": "N/A",
            "output_tokens": "N/A",
            "cost": "N/A",
            "endpoint": "/v1/chat/completions",
            "status": "No Activity",
            "inbox": "N/A",
            "timestamp": now,
            "message": "Menunggu aktivitas inference...",
            "action": "None"
        })

    return results

def save_to_json(results, output_file="inference_results.json"):
    """Simpan ke JSON untuk dashboard"""
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
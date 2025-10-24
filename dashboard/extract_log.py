import re
import json
import subprocess
import time
import os

def get_docker_logs():
    """Get logs from mounted Docker log directory with JSON"""
    try:
        # Detech container-ID 'kuzco-inference'
        result = subprocess.run(
            ['docker', 'ps', '-q', '-f', 'name=kuzco-inference'],
            capture_output=True,
            text=True,
            check=False
        )
        container_id = result.stdout.strip()
        if not container_id:
            print("DEBUG: No container found with name 'kuzco-inference'")
            return "No logs found"

        log_dir = "/host/docker/containers"
        log_file = os.path.join(log_dir, f"{container_id}/{container_id}-json.log")
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = f.read()
                print(f"DEBUG: Logs read from file {log_file} (first 500 chars) = {logs[:500]}...")
                print(f"DEBUG: Full log length = {len(logs)} characters")
                # Parse JSON lines and extract 'log' field
                log_entries = []
                for line in logs.splitlines():
                    try:
                        entry = json.loads(line)
                        if "log" in entry:
                            log_entries.append(entry["log"])
                    except json.JSONDecodeError:
                        continue
                return "\n".join(log_entries)
        else:
            print(f"DEBUG: Log file {log_file} not found")
            return "No logs found"
    except Exception as e:
        print(f"DEBUG: Unexpected error in get_docker_logs: {e}")
        return f"Error: {e}"

def extract_kuzco_results():
    """Extract Kuzco inference results from logs"""
    logs = get_docker_logs()
    results = []
    lines = [line.strip() for line in logs.split('\n') if line.strip()]

    print(f"DEBUG: Total lines processed = {len(lines)}")
    for line in lines:
        cleaned_line = re.sub(r'^\[\w+\|\w+\]: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z \d ', '', line)
        print(f"DEBUG: Processed line (cleaned) = {cleaned_line}")
        if any(msg in cleaned_line for msg in [
            'Processing message', 'Sending lock message', 'Downloading generation request',
            'Received lock response', 'Successfully downloaded generation request',
            'Starting streaming inference', 'Starting inference request',
            'SUCCESS: Streaming inference completed', 'Skipping logprobs'
        ]):
            time_match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)', line)
            timestamp = time_match.group(1) if time_match else "Unknown"
            inbox_match = re.search(r'inbox: (dispatcher\.[a-zA-Z0-9_\.]+)', line)
            inbox_id = inbox_match.group(1) if inbox_match else "N/A"
            if 'SUCCESS: Streaming inference completed' in cleaned_line:
                status, message, action = 'Completed', 'SUCCESS: Streaming inference completed', 'Inference'
            elif 'Skipping logprobs' in cleaned_line:
                status, message, action = 'Completed', 'Skipping logprobs', 'Inference'
            elif 'Sending lock message' in cleaned_line:
                status, message, action = 'Processing', 'Sending lock message', 'Lock'
            elif 'Received lock response' in cleaned_line:
                status, message, action = 'Processing', 'Received lock response', 'Lock'
            elif 'Downloading generation request' in cleaned_line:
                status, message, action = 'Processing', 'Downloading generation request', 'Download'
            elif 'Successfully downloaded generation request' in cleaned_line:
                status, message, action = 'Processing', 'Successfully downloaded generation request', 'Download'
            elif 'Starting streaming inference' in cleaned_line:
                status, message, action = 'Processing', 'Starting streaming inference', 'Inference'
            elif 'Starting inference request' in cleaned_line:
                status, message, action = 'Processing', 'Starting inference request', 'Inference'
            else:
                status, message, action = 'Processing', 'Processing message', 'Processing'
            try:
                dt = timestamp.split("T")[0] + " " + timestamp.split("T")[1].split(".")[0]
            except:
                dt = "N/A"
            results.append({
                "date": dt,
                "model": "llama-3.2-3b-instruct",
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
            print(f"DEBUG: Extracted - Timestamp: {timestamp}, Message: {message}, Inbox: {inbox_id}")
    results.sort(key=lambda x: x['timestamp'] if x['timestamp'] != "Unknown" else "", reverse=True)
    results = results[:50]
    if not results:
        now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        results.append({
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "model": "llama-3.2-3b-instruct",
            "input_tokens": "N/A",
            "output_tokens": "N/A",
            "cost": "N/A",
            "endpoint": "/v1/chat/completions",
            "status": "No Activity",
            "inbox": "N/A",
            "timestamp": now,
            "message": "Waiting activity inferences!",
            "action": "None"
        })
        print("DEBUG: No results extracted - using fallback")
    return results

def save_to_json(results, output_file="/app/inference_results.json"):
    """Save extracted results to JSON file"""
    try:
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"DEBUG: Saved to {output_file} with {len(results)} entries")
    except Exception as e:
        print(f"DEBUG: Error saving to JSON: {e}")
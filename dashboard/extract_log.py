import re
import json
import os

def get_docker_logs():
    """Get logs from mounted Docker log directory kuzco-inference"""
    try:
        log_dir = "/host/docker/containers"
        if not os.path.exists(log_dir):
            print("DEBUG: Log directory /host/docker/containers not found")
            return "No logs found"

        container_dirs = [d for d in os.listdir(log_dir) if os.path.isdir(os.path.join(log_dir, d))]
        if not container_dirs:
            print("DEBUG: No container directories found")
            return "No logs found"

        # Filter container 'kuzco-inference'
        for container_id in container_dirs:
            config_file = os.path.join(log_dir, container_id, "config.v2.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    # get container in-config
                    name = config.get("Name", "").lstrip("/")
                    if name == "kuzco-inference":
                        log_file = os.path.join(log_dir, container_id, f"{container_id}-json.log")
                        if os.path.exists(log_file):
                            with open(log_file, 'r') as log_f:
                                logs = log_f.read()
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
                            print(f"DEBUG: Log file {log_file} not found for container {container_id}")
                            return "No logs found"
        print("DEBUG: No container named 'kuzco-inference' found")
        return "No logs found"
    except Exception as e:
        print(f"DEBUG: Unexpected error in get_docker_logs: {e}")
        return f"Error: {e}"

def extract_kuzco_results():
    """Extract Kuzco inference results from sources logging"""
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
            inbox_id_full = inbox_match.group(1) if inbox_match else "N/A"
            # cutoff inbox_id text
            if inbox_id_full != "N/A" and len(inbox_id_full) > 20:  # cut if 20words
                inbox_id = inbox_id_full[:20] + "….INBOX.."
            else:
                inbox_id = inbox_id_full
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
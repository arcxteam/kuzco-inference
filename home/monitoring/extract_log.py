import re
import json
import os
import time

def extract_kuzco_results(log_file="/app/kuzco-inference/vikey-inference/kuzco.log"):
    results = []
    if not os.path.exists(log_file):
        return [{
            "date": "N/A",
            "model": "llama-3.2-3b-instruct-promo",  # Model start.sh
            "input_tokens": "N/A",
            "output_tokens": "N/A",
            "cost": "N/A",
            "endpoint": "/v1/chat/completions",
            "status": "Log file not found",
            "inbox": "N/A",
            "timestamp": "N/A",
            "message": "Log file not found"
        }]
    
    with open(log_file, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        match_time = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)', line)
        match_inbox = re.search(r'inbox: (\S+)', line)
        match_message = re.search(r'\[inference-cli\|[^\]]*?\]:.*?(Heartbeat response received|Starting streaming inference|SUCCESS: Streaming inference completed|Processing message|Sending lock message|Downloading generation request|Received lock response|Successfully downloaded generation request|Starting inference request|Skipping logprobs)(?: for inbox|$)', line)
        
        timestamp = match_time.group(1) if match_time else "Unknown"
        inbox_id = match_inbox.group(1) if match_inbox else "N/A"
        message = match_message.group(1) if match_message else line.strip()
        
        date = timestamp.split("T")[0] + " " + timestamp.split("T")[1].split(".")[0] if timestamp != "Unknown" else "N/A"
        
        # Parsing status
        status = "Completed" if "SUCCESS" in message else "Processing" if "Starting" in message or "Processing" in message else "Heartbeat" if "Heartbeat" in message else "Other"
        if "Ollama proxy server running" in message:
            status = "Proxy Running"
        
        results.append({
            "date": date,
            "model": "llama-3.2-3b-instruct-promo",
            "input_tokens": "N/A",
            "output_tokens": "N/A",
            "cost": "N/A",
            "endpoint": "/v1/chat/completions",
            "status": status,
            "inbox": inbox_id,
            "timestamp": timestamp,
            "message": message
        })
    
    if not results:
        results.append({
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "model": "llama-3.2-3b-instruct-promo",
            "input_tokens": "N/A",
            "output_tokens": "N/A",
            "cost": "N/A",
            "endpoint": "/v1/chat/completions",
            "status": "No inference completed yet",
            "inbox": "N/A",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
            "message": "No inference activity"
        })
    
    return results

def save_to_json(results, output_file="/app/monitoring/inference_results.json"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    results = extract_kuzco_results()
    save_to_json(results)
    print(f"Extracted {len(results)} inference results to inference_results.json")

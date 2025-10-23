#!/bin/bash

# use path binary
BINARY_PATH="/app/kuzco-inference/vikey-inference/vikey-inference-linux"
BINARY_DIR="/app/kuzco-inference/vikey-inference"

# verify binary exists
if [ ! -f "$BINARY_PATH" ]; then
    echo "Error: Binary CLI not found! Try Downloading..."
    mkdir -p "$BINARY_DIR"
    cd "$BINARY_DIR"
    wget https://github.com/arcxteam/kuzco-inference/releases/download/v1.0.0/vikey-inference-linux -O vikey-inference-linux
    chmod +x vikey-inference-linux
fi

# ran setup
"$BINARY_PATH" nvidia-smi --setup-gpu "GeForce RTX 4090"

# start services and capture all output
cd "$BINARY_DIR"
NODE_PORT=14444 DEFAULT_MODEL=llama3.2-3b-instruct nohup ./vikey-inference-linux 2>&1 | tee -a kuzco.log &
sleep 3
inference node start --code $CODE 2>&1 | tee -a kuzco.log &

# Debug: Verify kuzco.log
ls -l kuzco.log
cat kuzco.log

# Run monitoring
nohup python3 /app/monitoring/monitor_server.py > /app/monitoring.log 2>&1 &
echo "Monitoring started: Access http://ip-address:5050 for HTML dashboard"

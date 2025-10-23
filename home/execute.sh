#!/bin/bash

# use path binary
BINARY_PATH="/app/kuzco-inference/vikey-inference/vikey-inference-linux"
BINARY_DIR="/app/kuzco-inference/vikey-inference"

# verify binary
if [ ! -f "$BINARY_PATH" ]; then
    echo "Error: Binary CLI not found! Try Downloading..."
    mkdir -p "$BINARY_DIR"
    cd "$BINARY_DIR"
    wget https://github.com/arcxteam/kuzco-inference/releases/download/v1.0.0/vikey-inference-linux -O vikey-inference-linux
    chmod +x vikey-inference-linux
fi

# setup resources
"$BINARY_PATH" nvidia-smi --setup-gpu "GeForce RTX 4090"

# start kuzco service
cd "$BINARY_DIR"
NODE_PORT=14444 DEFAULT_MODEL=llama3.2-3b-instruct nohup ./vikey-inference-linux > kuzco.log 2>&1 &
sleep 3
inference node start --code $CODE
#!/bin/bash

# use path binary
BINARY_PATH="/app/kuzco-inference/vikey-inference/vikey-inference-linux"
BINARY_DIR="/app/kuzco-inference/vikey-inference"

# verify binary exists
if [ ! -f "$BINARY_PATH" ]; then
    echo "Error: Binary not found! Try Downloading..."
    mkdir -p "$BINARY_DIR"
    cd "$BINARY_DIR"
    wget https://github.com/direkturcrypto/vikey-inference/raw/main/vikey-inference-linux -O vikey-inference-linux
    chmod +x vikey-inference-linux
fi

# ran setup
"$BINARY_PATH" nvidia-smi --setup-gpu "GeForce RTX 4090"

# start services
cd "$BINARY_DIR"
NODE_PORT=14444 DEFAULT_MODEL=llama3.2-1b-instruct nohup ./vikey-inference-linux > kuzco.log 2>&1 &
sleep 3
inference node start --code $CODE
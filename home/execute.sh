#!/bin/bash

# Verify binary exists
if [ ! -f "/app/vikey-inference/vikey-inference-linux" ]; then
    echo "Error: Binary not found! Downloading..."
    wget https://github.com/direkturcrypto/vikey-inference/raw/main/vikey-inference-linux -O /app/vikey-inference/vikey-inference-linux
    chmod +x /app/vikey-inference/vikey-inference-linux
fi

# Run setup and start services
/app/vikey-inference/vikey-inference-linux nvidia-smi --setup-gpu "GeForce RTX 4090"
NODE_PORT=14444 DEFAULT_MODEL=llama3.2-3b-instruct nohup /app/vikey-inference/vikey-inference-linux > kuzco.log 2>&1 &
sleep 3
inference node start --code $CODE

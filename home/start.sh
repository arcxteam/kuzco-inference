#!/bin/bash

if [ "$1" == "serve" ]; then
    # Verify binary exists
    if [ ! -f "/app/vikey-inference/vikey-inference-linux" ]; then
        echo "Error: Binary not found! Downloading..."
        wget https://github.com/direkturcrypto/vikey-inference/raw/main/vikey-inference-linux -O /app/vikey-inference/vikey-inference-linux
        chmod +x /app/vikey-inference/vikey-inference-linux
    fi
    
    echo "Running Inference using Proxy"
    cd /app/vikey-inference && NODE_PORT=11434 DEFAULT_MODEL=llama3.2-8b-instruct ./vikey-inference-linux
else
    exit 1
fi

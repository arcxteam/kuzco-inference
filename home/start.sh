#!/bin/bash

if [ "$1" == "serve" ]; then
    # use path binary
    BINARY_PATH="/app/kuzco-inference/vikey-inference/vikey-inference-linux"
    BINARY_DIR="/app/kuzco-inference/vikey-inference"
    
    if [ ! -f "$BINARY_PATH" ]; then
        echo "Error: Binary not found! Try Downloading..."
        mkdir -p "$BINARY_DIR"
        cd "$BINARY_DIR"
        wget https://github.com/direkturcrypto/vikey-inference/raw/main/vikey-inference-linux -O vikey-inference-linux
        chmod +x vikey-inference-linux
    fi
    
    echo "Running Inference Model using Proxy"
    cd "$BINARY_DIR"
    NODE_PORT=14444 DEFAULT_MODEL=llama-3.2-1b-instruct ./vikey-inference-linux > vikey.log 2>&1
else
    exit 1
fi

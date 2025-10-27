#!/bin/bash

if [ "$1" == "serve" ]; then
    # use path binary
    BINARY_PATH="/app/kuzco-inference/vikey-inference/vikey-inference-linux"
    BINARY_DIR="/app/kuzco-inference/vikey-inference"
    
    if [ ! -f "$BINARY_PATH" ]; then
        echo "Error: Binary not found! Try Downloading..."
        mkdir -p "$BINARY_DIR"
        cd "$BINARY_DIR"
        wget https://github.com/arcxteam/kuzco-inference/releases/download/v1.0.0/vikey-inference-linux -O vikey-inference-linux
        chmod +x vikey-inference-linux
    fi
    
    echo "Start Running LLModels for Kuzco Inference w/ Proxy OpenrouterAi"
    cd "$BINARY_DIR"
    NODE_PORT=14444 DEFAULT_MODEL=llama-3.2-3b-instruct:free ./vikey-inference-linux > vikey.log 2>&1
else
    exit 1
fi

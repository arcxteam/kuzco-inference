#!/bin/bash

/app/vikey-inference/vikey-inference-linux nvidia-smi --setup-gpu "GeForce RTX 4090"
NODE_PORT=11434 DEFAULT_MODEL=llama3.2-3b-instruct nohup /app/vikey-inference/vikey-inference-linux > kuzco.log &
sleep 3
inference node start --code $CODE

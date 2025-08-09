FROM debian:stable-slim

RUN apt-get update && apt-get install -y curl systemd lsof procps git

WORKDIR /app
RUN mkdir -p /app/cache

RUN git clone https://github.com/arcxteam/kuzco-inference/vikey-inference
RUN cd vikey-inference && echo '["llama3.2:3b-instruct-fp16"]' > models.json

WORKDIR /app

RUN curl -fsSL https://devnet.inference.net/install.sh | sh

COPY ./start.sh /usr/local/bin/inference-runtime
COPY ./execute.sh /app/execute.sh
RUN chmod +x /app/execute.sh
RUN chmod +x /usr/local/bin/inference-runtime

# Jalankan Ollama Bridge dulu, lalu tunggu sampai siap sebelum Kuzco
CMD ["/app/execute.sh"]

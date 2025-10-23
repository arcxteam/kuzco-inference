FROM debian:stable-slim

RUN apt-get update && apt-get install -y curl systemd lsof procps git wget python3 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir -p /app/cache

# download binary
RUN git clone https://github.com/arcxteam/kuzco-inference && cd kuzco-inference/vikey-inference \
    && wget https://github.com/arcxteam/kuzco-inference/releases/download/v1.0.0/vikey-inference-linux -O vikey-inference-linux \
    && chmod +x vikey-inference-linux \
    && echo '["llama3.2:3b-instruct-fp16"]' > models.json

WORKDIR /app

RUN curl -fsSL https://devnet.inference.net/install.sh | sh

COPY ./start.sh /usr/local/bin/inference-runtime
COPY ./execute.sh /app/execute.sh
COPY .env .env
COPY ./monitoring /app/monitoring

RUN chmod +x /app/execute.sh
RUN chmod +x /usr/local/bin/inference-runtime
RUN pip3 install --no-cache-dir requests

CMD ["/app/execute.sh"]

FROM debian:stable-slim

RUN apt-get update && apt-get install -y wget git curl python3 python3-requests && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ARG VIKEY_API_KEY=your_default_api_key_here
ARG NODE_PORT=11434
# ARG EMBEDDING_API_URL=https://kuzco-inference.greyscope.xyz/v1
# ARG EMBEDDING_API_KEY=your_embedding_key_here

# Download binary
RUN wget https://github.com/arcxteam/kuzco-inference/releases/download/v1.0.0/vikey-inference-linux -O vikey-inference-linux \
    && chmod +x vikey-inference-linux

COPY models.json .
COPY .env .env

RUN if [ "$VIKEY_API_KEY" != "your_default_api_key_here" ]; then \
    sed -i "s/VIKEY_API_KEY=.*/VIKEY_API_KEY=$VIKEY_API_KEY/" .env; \
fi
RUN sed -i "s/NODE_PORT=.*/NODE_PORT=$NODE_PORT/" .env
# RUN echo "EMBEDDING_API_URL=$EMBEDDING_API_URL" >> .env
# RUN echo "EMBEDDING_API_KEY=$EMBEDDING_API_KEY" >> .env

EXPOSE $NODE_PORT

CMD ["./vikey-inference-linux"]

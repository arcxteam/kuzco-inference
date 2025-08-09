FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y wget

WORKDIR /app

ARG VIKEY_API_KEY=your_default_api_key_here
ARG NODE_PORT=11434

# Download binary api
RUN wget https://github.com/direkturcrypto/vikey-inference/raw/main/vikey-inference-linux -O vikey-inference-linux \
    && chmod +x vikey-inference-linux

COPY models.json .
COPY .env .env

RUN if [ "$VIKEY_API_KEY" != "your_default_api_key_here" ]; then \
    sed -i "s/VIKEY_API_KEY=.*/VIKEY_API_KEY=$VIKEY_API_KEY/" .env; \
  fi

RUN sed -i "s/NODE_PORT=.*/NODE_PORT=$NODE_PORT/" .env

EXPOSE $NODE_PORT

CMD ["./vikey-inference-linux"]

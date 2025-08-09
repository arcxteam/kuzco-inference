FROM debian:bullseye-slim

WORKDIR /app

ARG VIKEY_API_KEY=your_default_api_key_here
ARG NODE_PORT=11434

COPY vikey-inference-linux .
COPY models.json .
COPY .env .env

RUN chmod +x vikey-inference-linux

RUN if [ "$VIKEY_API_KEY" != "your_default_api_key_here" ]; then \
    sed -i "s/VIKEY_API_KEY=.*/VIKEY_API_KEY=$VIKEY_API_KEY/" .env; \
  fi

RUN sed -i "s/NODE_PORT=.*/NODE_PORT=$NODE_PORT/" .env

EXPOSE $NODE_PORT

CMD ["./vikey-inference-linux"] 

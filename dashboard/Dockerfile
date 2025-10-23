FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY extract_log.py monitor_server.py index.html ./

CMD ["python", "monitor_server.py"]
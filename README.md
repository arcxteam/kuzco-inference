# A Comprehensive Guide - Running Kuzco Inference with CPU by API Proxy (Ollama or OpenAI)


## Inferences System Data Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant KuzcoWorker
    participant VikeyAPI
    participant AIModel
    
    Client->>KuzcoWorker: Request AI Service
    KuzcoWorker->>VikeyAPI: Call Inference API
    VikeyAPI->>AIModel: Process Request
    AIModel->>VikeyAPI: Return Inference Result
    VikeyAPI->>KuzcoWorker: Send API Response
    KuzcoWorker->>Client: Deliver Final Result
```

## Structure Directory of File

```diff
/kuzco-inference
├──.dockerignore
├──.ignore
│
├── /home
│   ├── monitoring/
│   │   ├── extract_log.py
│   │   ├── index.html
│   │   ├── monitor_server.py
│   │   └── inference_results.json
│
│   ├── .env
│   ├── .gitignore
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   ├── ex.nginx-conf
│   ├── execute.sh
│   └── start.sh
│
├── /vikey-inference
│   ├── .env
│   ├── .gitignore
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   ├── models.json
│   └── vikey-inference-linux            # File binary for linux
│
├── README.md
```

## Config Account

Copy .env from example
```bash
cp .env.example .env
```
Edit `.env`:
```
nano .env
```

## Flowchart Distribution

```mermaid
graph TD
    A[USER] --> B[RUNNER]
    B --> C[DOCKER]
    C --> D1[Build vikey-inference]
    C --> D2[Build home-main]
    
    D1 --> E1[Download binary dari GitHub]
    D1 --> F1[Konfigurasi .env]
    D1 --> G1[Build Image]
    
    D2 --> E2[Download binary ke /app/vikey-inference]
    D2 --> F2[Install Inference Runtime]
    D2 --> G2[Build Image]
    
    G1 --> H1[Run Container]
    G2 --> H2[Run Container]
    
    H1 --> I1[Start Vikey API<br>Port 11434]
    H2 --> I2[Execute execute.sh]
    
    I2 --> J{Verify Binary}
    J -->|Missing| K[Download binary]
    J -->|Exists| L[Setup GPU & Model]
    
    L --> M[Start Inference Service]
    M --> N[Kuzco.log]
    
    I2 --> O[Start Kuzco Node<br>--code $CODE]
    
    I1 --> P[[Vikey Inference API]]
    O --> Q[[Kuzco Worker]]
    
    P --> R[[Handle AI Requests]]
    Q --> S[[Manage Workers]]
    
    R --> T[AI Responses]
    S --> U[Coordinate Jobs]
    
    style A fill:#4CAF50,stroke:#388E3C
    style P fill:#2196F3,stroke:#0D47A1
    style Q fill:#FF9800,stroke:#E65100
    style R fill:#9C27B0,stroke:#6A1B9A
    style T fill:#F44336,stroke:#D32F2F
```

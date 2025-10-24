# A Comprehensive Guide - Running Kuzco Inference with CPU by API Proxy (Ollama or OpenAI)

## (1) Inferences System Data Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant KuzcoWorker
    participant VikeyAPI
    participant Model/AI
    
    Client->>KuzcoWorker: Request AI Service
    KuzcoWorker->>VikeyAPI: Call Inference API
    VikeyAPI->>Model/AI: Process Request
    Model/AI->>VikeyAPI: Return Inference Result
    VikeyAPI->>KuzcoWorker: Send API Response
    KuzcoWorker->>Client: Deliver Final Result
```

## (2) Structure Directory of File

```diff
/kuzco-inference
├──.dockerignore
├──.ignore
│
├── /home
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
├── /dashboard                           # Web realtime monitoring (optional)
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   ├── extract_log.py
│   ├── index.html                       # Homepages (access ip-server:port)
│   ├── monitor_server.py
│   └── inference_results.json
│
└── README.md
```

---

## Initial Requirements

| Requirement     | Minimum                |
| :----------     | :--------------------  |
| **Linux**       | Ubuntu 20 - 22 - 24 LTS          |
| **Mac**         | Chip M1, M2, M3, M4              |
| **CPU**         | vCores 8 with 8GB RAM - more     |      
| **STORAGE**     | Up 50GB - 99GB - more spaces     |

## Dashboard Registration

### Register and Obtain an API Key
- Visit the dashboard & sign up using an email:
- Navigate to the `API-KEYS` section.
- Create a new key `wsk-xxx` **SAVE SAVE SAVE**
- Copy the key you can create multiple keys, **if forget save generate again**
- 
## Clone Repository

```bash
git clone https://github.com/arcxteam/kuzco-inference.git
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

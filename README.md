# A Comprehensive Guide - Running Kuzco Inference with CPU by API Proxy (Ollama or OpenAI)

<img width="1600" height="900" alt="Run Testnet" src="https://github.com/user-attachments/assets/d647bd9f-7fea-47c3-9e46-67940e42e1df" />

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

## (2) Structure Directory

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
-├── /dashboard                          # Realtime monitoring run (optional)
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   ├── extract_log.py
│   ├── index.html                       # Homepage (check preview)
│   ├── monitor_server.py
│   └── inference_results.json
│
└── README.md
```

## (3) Preview/Demo Kuzco Inference Homepage

> [!NOTE]
> Check preview homepage if need run (realtime) by own-localthost [Kuzco Inference Dashboard](https://arcxteam.github.io/kuzco-inference/dashboard/)

---

## A. SETUP FOR ACCOUNT

![VPS](https://img.shields.io/badge/VPS/SERVER-232F3E?style=for-the-badge&logo=digitalocean&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

### 1. Initial Requirements

| Requirement     | Details                |
| :----------     | :--------------------  |
| **Linux**       | Ubuntu 20 - 22 - 24 LTS          |
| **CPU**         | vCores 8 with 8GB RAM - more     |      
| **STORAGE**     | Up 50GB - more spaces            |
| **API PROXY**   | Support LLM Ollama & OpenAI      |
| **PORT**        | Open 11434 (Official API Proxy)  |
|                 | Open 14444 (Official API Kuzco)  |
|                 | Open 5050 (Custom for Dashboard) |

### 2. Registration Kuzco Inference

**Obtain correct CLI WORKER**
- Sign up here https://devnet.inference.net/register
- Navigate to [create worker](https://devnet.inference.net/dashboard/workers/create)
- Create up to you `Worker Name` → `CLI` → `Create Worker`
- Click your `Worker Name` → click `Instance` and `Launch worker` → in section Step 2: Run an instance of this worker `COPY YOUR CODE`

### 3. Registration for API Proxy
**Note, use Vikey AI**
- Need API-KEY w/ compatible format Ollama or OpenAI (LLM)
- I use `VikeyAI` for default Kuzco model `llama-3.2-3b-instruct` & more models <mark>Rp.3000-5000/1M Tokens ~ $0.2-$0.3/1M Tokens</mark>
- Readme here for detail use [bahasa indonesia](https://github.com/arcxteam/kuzco-inference/blob/main/VIKEY-ID.md)
- Readme here for detail use [languange english](https://github.com/arcxteam/kuzco-inference/blob/main/VIKEY-EN.md)

## B. SETUP FOR CONFIGURATION

### 1. Update System Packages
```bash
sudo apt update && sudo apt upgrade -y && \
sudo apt install screen curl ufw nload tree iptables git wget lz4 jq make gcc nano automake autoconf \
htop tmux libgbm1 protobuf-compiler python3 python3-pip python3-venv python3-dev python3-setuptools \
tar clang nethogs ncdu unzip build-essential pkg-config libssl-dev libleveldb-dev \
speedtest-cli ca-certificates libffi-dev libsqlite3-dev -y
```

### 2. Install Node.js, Npm, Yarn, & Pm2 (optional)
```
source <(wget -qO- https://raw.githubusercontent.com/arcxteam/w-ai-wombo/main/nodejs.sh)
```

### 3. Install Docker & Compose → <mark>if not yet</mark>
```bash
curl -sSL https://raw.githubusercontent.com/arcxteam/succinct-prover/refs/heads/main/docker.sh | bash
```

### 4. Clone Repository & PORT Firewall
```bash
git clone https://github.com/arcxteam/kuzco-inference.git
```

```bash
sudo ufw allow 11434 && sudo ufw allow 14444 && sudo ufw allow 5050 && sudo ufw reload && sudo ufw status verbose
```

> After completed all step above, final config for step running 

- Setup directory `kuzco-inference/home/` **(Main Run Kuzco)**
- Setup directory `kuzco-inference/vikey-inference/` **(API Proxy Model Run)**
- Setup directory `kuzco-inference/dashboard/` **(optional run if need realtime monitoring)**

### 5. Config Account (.env)

> NOTE: RUN 1st
- First need running `API Proxy LLModel Running`
- Replace this API KEY `VIKEY_API_KEY=vk-xxxxxxxxx`
- If success build check logs `docker compose logs` this optional

```bash
cd kuzco-inference/vikey-inference && nano .env
```

```bash
docker compose up --build -d
```

> NOTE: RUN 2nd
- Seconds need running `Main Run Kuzco with official config Binary`
- After success run above, in terminal back to `cd` and next step
- Replace this `WORKER_CODE=xxxxxxx` and `WORKER_NAME=xxxxxx` and `VIKEY_API_KEY=vk-xxxxxx`
- Where do? worker code, worker name read above **A.SETUP FOR ACCOUNT**

```bash
cd kuzco-inference/home && nano .env
```

```bash
docker compose up --build -d
```

### 6. Running Homepages/Dashboard

> NOTE: AFTER SUCCESS RUN ALL AND STABLE GET INFERENCE INFO LOGGING, YOU CAN RUNNING YOUR OWN DASHBOARD MONITORING THIS ACTUALLY YOUR OWN RUNNING LOGS
- Get ip address `curl ifconfig.me && echo`
- For access `http://ip-address:5050`

```bash
cd kuzco-inference/dashboard && docker compose up --build -d
```


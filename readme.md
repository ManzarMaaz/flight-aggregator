
# ✈️ Distributed Flight Aggregator

### Async Flight Tracking • AI Policy Engine • RAG Assistant • Distributed Task Processing

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=009688&center=true&vCenter=true&width=1000&lines=Distributed+Flight+Aggregator;FastAPI+%7C+Celery+%7C+Redis+%7C+pgvector;RAG+Policy+Engine+%7C+Gemini+AI+%7C+Docker;Async+%7C+Containerized+%7C+Microservices" />

<p>
  <img src="https://img.shields.io/badge/FastAPI-Async-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Celery-Distributed-37814A?style=for-the-badge&logo=celery&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-Message%20Broker-DC382D?style=for-the-badge&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

<p>
  <img src="https://img.shields.io/badge/Gemini-AI%20Powered-4285F4?style=flat-square&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/LlamaIndex-RAG-FF6F00?style=flat-square" />
  <img src="https://img.shields.io/badge/Docker-Multi--Container-2496ED?style=flat-square&logo=docker" />
  <img src="https://img.shields.io/badge/Twilio-SMS-F22F46?style=flat-square&logo=twilio&logoColor=white" />
  <img src="https://img.shields.io/badge/Gmail-SMTP-EA4335?style=flat-square&logo=gmail&logoColor=white" />
</p>

<img src="https://capsule-render.vercel.app/api?type=rect&height=2&color=009688" width="100%" />

</div>

---

<p align="center">
  <img src="assets/banner.png" alt="Distributed Flight Aggregator Banner" width="100%">
</p>

# ⚡ Overview

A production-oriented, fully containerized **distributed flight monitoring and policy intelligence platform** built with **FastAPI**, **Celery**, **Redis**, and **PostgreSQL + pgvector**.

The platform continuously monitors flight destinations, polls the **Amadeus API** for real-time flight offers, automatically resolves city names to airport IATA codes, compares prices against user-defined thresholds, and dispatches notifications through **Twilio SMS** and **Gmail SMTP**.

Beyond flight tracking, the application incorporates an **AI-powered Retrieval-Augmented Generation (RAG) engine** using **LlamaIndex** and **Gemini**, enabling semantic policy searches and a conversational flight assistant.

This project isn't just an API demo—it's a practical exercise in building distributed systems, asynchronous task execution, AI integration, vector databases, and production-ready containerized infrastructure. 

---

# ✨ Features

* ✈️ Real-time flight monitoring via Amadeus API
* 🌍 Automatic City → IATA code resolution
* 💰 User-defined target price tracking
* 📨 Dual-channel notifications (SMS + Email)
* ⚡ Asynchronous task execution with Celery
* 🧠 AI-powered Flight Policy RAG Engine
* 💬 Conversational Flight Assistant CLI
* 🔍 Semantic document search using pgvector
* 📦 Fully containerized microservice architecture
* ⏰ Scheduled flight sweeps via Celery Beat
* 🚀 Distributed worker infrastructure
* 🐳 Docker Compose orchestration
* 📊 Infrastructure logging and diagnostics

---

# 🏗️ Architecture

```mermaid
graph TD
    A[API Consumers / CLI] --> B[FastAPI App]

    B --> C[PostgreSQL + pgvector]
    B --> D[Redis Broker]

    D --> E[Celery Worker]
    D --> F[Celery Beat]

    E --> G[Amadeus API]
    E --> H[Twilio SMS]
    E --> I[Gmail SMTP]

    B --> J[LlamaIndex]
    J --> K[Gemini AI]
    J --> C

    F --> E
```

---

# ⚙️ Tech Stack

| Layer             | Technology          | Purpose                                     |
| ----------------- | ------------------- | ------------------------------------------- |
| Framework         | FastAPI             | High-performance asynchronous API framework |
| AI Framework      | LlamaIndex          | RAG orchestration and retrieval pipelines   |
| LLM               | Gemini 2.5 Flash    | Contextual responses and reasoning          |
| Embeddings        | Gemini Embedding-2  | Semantic vector generation                  |
| Database          | PostgreSQL 15       | Persistent relational storage               |
| Vector Store      | pgvector            | Embedding storage and similarity search     |
| ORM               | SQLAlchemy          | Database abstraction and transactions       |
| Cache / Broker    | Redis 7             | Task queue broker and caching               |
| Distributed Tasks | Celery              | Background processing and scheduling        |
| Scheduler         | Celery Beat         | Automated periodic execution                |
| HTTP Client       | Httpx               | Async API communication                     |
| Notifications     | Twilio + Gmail SMTP | SMS and Email delivery                      |
| Infrastructure    | Docker + Compose    | Multi-container orchestration               |

---

# 🏛️ System Services

| Service        | Container              | Responsibility                                             |
| -------------- | ---------------------- | ---------------------------------------------------------- |
| API Gateway    | `flight_fastapi`       | Routing, validation, destination management, RAG endpoints |
| Database       | `flight_postgres`      | Relational storage and vector embeddings                   |
| Message Broker | `flight_redis`         | Task queue communication and caching                       |
| Worker Cluster | `flight_celery_worker` | Flight polling, AI processing, notifications               |
| Scheduler      | `flight_celery_beat`   | Automated flight monitoring schedules                      |

---

# 🛣️ API Endpoints

## Destinations

| Method   | Endpoint                      | Description                        |
| -------- | ----------------------------- | ---------------------------------- |
| `POST`   | `/api/v1/destinations/create` | Create flight tracking destination |
| `GET`    | `/api/v1/destinations`        | Retrieve tracked destinations      |
| `PUT`    | `/api/v1/destinations/{id}`   | Update destination                 |
| `DELETE` | `/api/v1/destinations/{id}`   | Remove destination                 |

---

## Flight Analysis

| Method | Endpoint                       | Description                   |
| ------ | ------------------------------ | ----------------------------- |
| `POST` | `/api/v1/flights/analyze-deal` | Analyze flight deals using AI |
| `GET`  | `/api/v1/flights/offers`       | Retrieve flight offers        |

---

## AI Policy Engine

| Method | Endpoint         | Description                     |
| ------ | ---------------- | ------------------------------- |
| `POST` | `/ai/ask-policy` | Semantic flight policy Q&A      |
| `POST` | `/ai/chat`       | Conversational flight assistant |

---

# ✈️ Flight Monitoring Workflow

```text
User Creates Destination
            ↓
City Name → IATA Resolution
            ↓
Store Destination in PostgreSQL
            ↓
Celery Beat Scheduler Trigger
            ↓
Celery Worker Polls Amadeus API
            ↓
Price Comparison Against Threshold
            ↓
AI Deal Analysis
            ↓
SMS + Email Notifications
```

---

# 🧠 Retrieval-Augmented Generation (RAG)

The application includes a semantic policy engine powered by:

```text
Flight Policy Documents
            ↓
Chunking & Embedding
            ↓
Gemini Embedding-2
            ↓
pgvector Storage
            ↓
Similarity Search
            ↓
LlamaIndex Retrieval
            ↓
Gemini Response Generation
```

Users can ask questions like:

* What is the pet transport policy?
* What happens during flight cancellation?
* Are refunds available for missed flights?
* What baggage restrictions apply?

The system returns contextual answers with source citations and relevance scores.

---

# 🔐 Notification System

Price alerts are delivered through two independent channels:

### SMS Alerts

* Twilio API
* Near real-time delivery
* Threshold breach notifications

### Email Alerts

* Gmail SMTP
* Rich formatted messages
* Detailed flight offer information

Dual-channel delivery increases reliability and reduces the chance of users missing important price drops.

---

# ⚡ Distributed Architecture

The application separates workloads across multiple services:

### FastAPI

* Request handling
* Validation
* API lifecycle management
* AI endpoint orchestration

### Celery Workers

* Flight API polling
* Price comparison
* AI analysis
* Notification dispatch

### Redis

* Message broker
* Task queue
* Temporary cache

### PostgreSQL + pgvector

* Transactional data
* User preferences
* Destination tracking
* Semantic embeddings

This separation prevents long-running I/O operations from blocking API requests and enables horizontal scaling.

---

# 🗄️ Vector Database Ingestion

Populate the vector database:

```bash
docker-compose exec flight_fastapi python ingest.py
```

The ingestion process:

1. Reads documents from `./data`
2. Splits documents into chunks
3. Generates embeddings using Gemini
4. Stores vectors in PostgreSQL
5. Enables semantic retrieval for RAG queries

---

# 🐳 Multi-Container Infrastructure

```text
FastAPI Container
        │
        ├── PostgreSQL + pgvector
        ├── Redis
        ├── Celery Worker
        └── Celery Beat
```

Every component is independently deployable and replaceable, making the system resilient and easier to scale.

---

# 🚀 Getting Started

## Prerequisites

* Docker & Docker Desktop
* Python 3.11+
* Git

---

## Clone Repository

```bash
git clone https://github.com/ManzarMaaz/flight-aggregator.git

cd flight-aggregator
```

---

## Configure Environment

```env
DATABASE_URL=postgresql://admin:supersecretpassword@flight_postgres:5432/flight_db

REDIS_HOST=flight_redis
REDIS_PORT=6379
REDIS_URL=redis://flight_redis:6379/0

GEMINI_API_KEY=your_api_key

AMADEUS_API_KEY=your_key
AMADEUS_API_SECRET=your_secret

SMTP_SERVER=smtp.gmail.com
MY_MAIL=your_email
MY_PASS=your_app_password

TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_VIRTUAL_NUMBER=+1XXXXXXXXXX
TWILIO_VERIFIED_NUMBER=+91XXXXXXXXXX
```

---

## Start Infrastructure

```bash
docker-compose up -d --build
```

Verify services:

```bash
docker ps
```

---

## Run Ingestion

```bash
docker-compose exec flight_fastapi python ingest.py
```

---

## Launch CLI Assistant

```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python cli_client.py
```

---

## Swagger Documentation

Visit:

```text
http://127.0.0.1:8000/docs
```

---

# 📊 Infrastructure Monitoring

### FastAPI Logs

```bash
docker logs -f flight_fastapi
```

### Worker Logs

```bash
docker logs -f flight_celery_worker
```

### Scheduler Logs

```bash
docker logs -f flight_celery_beat
```

---

# ⚖️ Engineering Decisions

### Why Celery + Redis?

Flight polling and AI analysis are long-running I/O tasks. Offloading them prevents blocking API requests and allows independent scaling.

### Why pgvector?

Flight policy queries require semantic retrieval rather than keyword matching. Vector search enables contextual question answering.

### Why Gemini + LlamaIndex?

LlamaIndex provides document orchestration while Gemini delivers embeddings and contextual generation with structured outputs.

### Why Docker Compose?

The application consists of multiple cooperating services. Container orchestration ensures reproducible local environments and production parity.

### Why Dual Notifications?

SMS and Email redundancy significantly improve alert reliability for time-sensitive flight deals.

---

# 📈 Future Improvements

* [ ] JWT Authentication
* [ ] Multi-user accounts and preferences
* [ ] Flight history analytics dashboard
* [ ] Airline recommendation engine
* [ ] Kubernetes deployment
* [ ] OpenTelemetry instrumentation
* [ ] Prometheus metrics
* [ ] Grafana dashboards
* [ ] Distributed tracing
* [ ] WebSocket live notifications
* [ ] Refresh token support
* [ ] Multi-region deployment
* [ ] CI/CD via GitHub Actions
* [ ] Flight recommendation ML models
* [ ] Dynamic pricing prediction

---

# 👨‍💻 Author

**Mohammed Manzar Maaz**

<p>
  <a href="https://github.com/ManzarMaaz">
    <img src="https://img.shields.io/github/followers/ManzarMaaz?label=Follow&style=social" />
  </a>
  <a href="https://www.linkedin.com/in/mohammed-manzar-maaz">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin" />
  </a>
</p>

<br>

<div align="center">
<i>Built to practice distributed systems engineering, asynchronous task processing, vector databases, AI-powered retrieval, and production-grade microservice architecture.</i>
</div>

---

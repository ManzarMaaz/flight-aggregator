
---

# ✈️ Distributed Flight Aggregator & Alert Engine

An enterprise-grade, fully containerized asynchronous flight tracking application built on **FastAPI**, distributed with **Celery** and **Redis**, backed by **PostgreSQL**, and automated via **Celery Beat**.

The application monitors specified flight destinations, polls the real-time **Amadeus API** for prices, checks them against customized target thresholds, and instantly coordinates dual-channel alerts via **Twilio SMS** and **Gmail SMTP**.

---

## 🏗️ System Architecture

The application is engineered as a decoupled microservice cluster split across 5 specialized Docker containers:

* **FastAPI App (`flight_fastapi`)**: High-performance, low-latency asynchronous API server providing the endpoint definitions and Swagger documentation.
* **PostgreSQL (`flight_postgres`)**: Relational database storing destination targets, thresholds, active flags, and tracking historical logs.
* **Redis (`flight_redis`)**: In-memory data store acting as the message broker passing asynchronous task states between the API and backend workers.
* **Celery Worker (`flight_celery_worker`)**: Distributed execution thread cluster running the heavy compute workloads (Amadeus API calls and notification dispatches).
* **Celery Beat (`flight_celery_beat`)**: Heartbeat clock scheduler injecting cron triggers into Redis to keep the entire engine running completely on autopilot.

---

## 🛠️ Tech Stack

| Technology | Layer | Purpose |
| --- | --- | --- |
| **FastAPI** | Web Framework | Request validation & routing |
| **SQLAlchemy** | ORM | Database interaction abstraction |
| **PostgreSQL 15** | Database | Core application persistence |
| **Redis 7** | Message Broker | Task queue pipelines |
| **Celery** | Worker Engine | Distributed asynchronous processing |
| **Httpx** | Async HTTP Client | Non-blocking third-party API polling |
| **Docker / Compose** | Infrastructure | Unified ecosystem virtualization |

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have the following installed on your machine:

* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Git](https://git-scm.com/)

### 2. Environment Configuration

Create a `.env` file in the root directory right next to `docker-compose.yml` and populate your live credentials:

```env
# Database Settings
DATABASE_URL=postgresql://admin:supersecretpassword@db:5432/flight_db

# Redis Broker Settings
REDIS_URL=redis://redis:6379/0

# Amadeus API Credentials
AMADEUS_API_KEY=your_amadeus_api_key
AMADEUS_API_SECRET=your_amadeus_api_secret
TOKEN_ENDPOINT=https://test.api.amadeus.com/v1/security/oauth2/token
CITY_SEARCH_ENDPOINT=https://test.api.amadeus.com/v1/reference-data/locations
FLIGHT_ENDPOINT=https://test.api.amadeus.com/v2/shopping/flight-offers

# Notification Credentials
SMTP_SERVER=smtp.gmail.com
MY_MAIL=your_gmail_address@gmail.com
MY_PASS=your_16_digit_gmail_app_password
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_VIRTUAL_NUMBER=+1XXXXXXXXXX
TWILIO_VERIFIED_NUMBER=+91XXXXXXXXXX

```

### 3. Spin Up the Ecosystem

Launch all services simultaneously with a single multi-threaded build command:

```bash
docker-compose up -d --build

```

Verify that all 5 elements of your cluster are healthy:

```bash
docker ps

```

---

## 🕹️ API & Usage Guide

Once the containers are online, your API is exposed locally on port `8000`.

* **Interactive Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)
* **Alternative Documentation (Redoc)**: [http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc)

### Core Workflows

1. **Inject a Target Destination**: Use `POST /api/v1/destinations/create` to add tracking targets (e.g., `Paris (CDG)`, Target: `50000`).
2. **Verify Active Trackers**: Use `GET /api/v1/destinations/list` to inspect target states.
3. **Trigger On-Demand Tracking**: Use `POST /api/v1/track-flights` to force an immediate task execution offloaded onto Celery.
4. **Autopilot Routine**: Celery Beat will automatically fire the tracking routine every morning at **8:00 AM (Asia/Kolkata)** without any user interaction.

---

## 📊 Infrastructure Monitoring & Diagnostics

To trace logic execution, catch rate limit defenses (HTTP 429), or track email/SMS dispatches, stream the logs directly from the running containers:

* **Monitor Main Worker Processes (Flight Search & Deals)**:
```bash
docker logs -f flight_celery_worker

```


* **Monitor API Server (HTTP traffic)**:
```bash
docker logs -f flight_fastapi

```


* **Monitor Scheduler Activity (Cron Heartbeat)**:
```bash
docker logs -f flight_celery_beat

```



To halt the environment entirely without losing persistent volumes:

```bash
docker-compose down

```

To purge database records alongside the containers:

```bash
docker-compose down -v

```

# Arcadia Insights

> Life is Strange Choice Analytics Platform - Data engineering & ML platform for player behavior analysis using **Clean Architecture** and **Event-Driven Design**.

---

## Overview

Data analytics platform that collects, processes, and analyzes millions of player decisions from the Life is Strange franchise, generating behavioral insights, global statistics, and predictions using Machine Learning.

**Portfolio project demonstrating:**

- Distributed Systems Architecture
- Data Engineering at scale
- Machine Learning pipelines
- Data Lake & Data Warehouse Design
- Event-Driven Architecture
- Real-time Analytics

---

## Stack

| Component        | Tool                         | Purpose                          |
| ---------------- | ---------------------------- | -------------------------------- |
| Backend API      | **FastAPI** + **SQLAlchemy** | REST API with Clean Architecture |
| Frontend         | **Next.js 15** + TypeScript  | Web application                  |
| Message Broker   | **Apache Kafka 7.6.0**       | Event streaming                  |
| Orchestration    | **Apache Airflow 2.9.0**     | Workflow management              |
| Processing       | **Apache Spark** (PySpark)   | Batch & stream processing        |
| OLTP Database    | **PostgreSQL 16**            | Operational data                 |
| OLAP Database    | **ClickHouse 24**            | Analytical queries               |
| Cache            | **Redis 7**                  | Caching layer                    |
| Object Storage   | **MinIO** (S3-compatible)    | Data Lake (Bronze/Silver/Gold)   |
| Monitoring       | **Prometheus** + **Grafana** | Metrics & observability          |
| Containerization | **Docker Compose**           | Local development environment    |

---

## Quick Start

### Prerequisites

- Docker Desktop installed and running
- Python 3.13+ installed
- 8GB+ RAM available
- 10GB+ disk space

### Setup & Run

```bash
# 1. Clone and setup
git clone https://github.com/your-username/arcadia-insights.git
cd arcadia-insights
cp .env.example .env

# 2. Start infrastructure
docker compose up -d

# Wait ~30 seconds for services to start

# 3. Setup API
cd c_api
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -e ".[dev]"

# 4. Run API
uvicorn src.main:app --reload
```

### Access Services

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (admin: arcadia-admin / arcadia-secret-key-123)
- **Airflow**: http://localhost:8080 (admin / admin)
- **Grafana**: http://localhost:3001 (admin / admin)
- **Prometheus**: http://localhost:9090

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Create player
curl -X POST http://localhost:8000/api/v1/players/ \
  -H "Content-Type: application/json" \
  -d '{"country": "BR", "platform": "PC", "game_version": "1.0.0"}'
```

---

## Features

**Player Features:**

- Upload game saves
- Personal dashboard with choice analysis
- Global community comparison
- Ending prediction based on decisions
- Player profile classification (Empathetic, Utilitarian, etc.)

**Analytics Features:**

- Real-time global statistics
- Geographic distribution of choices
- Narrative pattern analysis
- Machine Learning clustering and prediction

---

## Architecture

```
┌─────────────┐
│   Jogador   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                        │
│  Home │ Upload │ Dashboard │ Global Stats │ Insights         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 Backend API (FastAPI)                        │
│          Clean Architecture + DDD + SOLID                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Message Broker (Kafka)                     │
│              Event-Driven Architecture                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 Data Lake (MinIO/S3)                         │
│            Bronze │ Silver │ Gold Layers                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Orchestration (Apache Airflow)                  │
│                    ETL/ELT Pipelines                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Processing (Apache Spark)                       │
│          Batch & Streaming Analytics                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌──────────────────────┬──────────────────────────────────────┐
│   PostgreSQL         │        ClickHouse                     │
│ Operational Data     │    Analytical Queries                │
└──────────────────────┴──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│         Visualization (Streamlit + Custom Dashboards)        │
└─────────────────────────────────────────────────────────────┘
```

See full documentation at [k_docs/architecture/](k_docs/architecture/README.md)

---

## Project Structure

Top-level folders follow a `<letter>_<name>` ordering pattern so they
appear in the logical data-flow order in the file tree.

```
arcadia-insights/
├── a_configs/             # Settings, configs, factories
├── b_models/              # Pydantic models, Spark schemas
├── c_api/                 # Backend API (FastAPI + Clean Architecture)
│   ├── src/
│   │   ├── domain/            # Entities, Value Objects, Repositories
│   │   ├── application/       # Use Cases, DTOs
│   │   ├── infrastructure/    # DB, Kafka, Redis, S3 adapters
│   │   └── presentation/      # API routes, middleware
│   ├── tests/
│   └── pyproject.toml
├── d_web/                 # Frontend (Next.js 15 + TypeScript)
├── e_kafka/               # Kafka producers & consumers
├── f_spark/               # PySpark jobs (Bronze → Silver → Gold)
│   └── jobs/
├── g_storage/             # Storage adapters (Parquet, Delta, DB)
├── h_airflow/             # Airflow DAGs & orchestration
│   ├── dags/
│   ├── logs/
│   └── plugins/
├── i_ml/                  # Machine Learning models & pipelines
├── j_infrastructure/      # Docker configs, deployments
│   ├── postgres/
│   ├── clickhouse/
│   └── grafana/
├── k_docs/                # Documentation & ADRs
│   └── architecture/
│       └── decisions/
├── l_scripts/             # Setup & utility scripts
├── m_data/                # Local data storage (gitignored)
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── z_tests/               # Integration & e2e tests
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

---

## Development

### Code Standards

**Python:**

- Follow PEP 8
- Use type hints
- Write docstrings
- Maintain Clean Architecture principles
- Test coverage > 80%

**Commit Messages:**
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add player profile clustering
fix: resolve save upload timeout
docs: update architecture diagrams
test: add tests for choice statistics
```

### Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test
pytest z_tests/unit/test_player.py
```

### Docker Commands

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f

# Restart specific service
docker compose restart postgres
```

---

## Troubleshooting

### Port already in use

```bash
# Linux/Mac
lsof -i :8000

# Windows
netstat -ano | findstr :8000
```

### Docker not running

- Start Docker Desktop
- Verify: `docker info`

### Services not starting

- Check logs: `docker compose logs`
- Verify ports are available
- Ensure sufficient RAM (8GB+)

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest`
5. Commit: `git commit -m 'feat: add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

---

## Documentation

- **Architecture**: [k_docs/architecture/](k_docs/architecture/README.md)
- **API Docs**: http://localhost:8000/docs (when running)
- **ADRs**: [k_docs/architecture/decisions/](k_docs/architecture/decisions/)

---

## Skills Demonstrated

- Clean Architecture + DDD
- Event-Driven Architecture
- Data Lake (Bronze/Silver/Gold)
- ETL/ELT Pipelines
- OLTP + OLAP Databases
- Stream Processing
- Machine Learning Pipeline
- DevOps & Observability

---

## License

MIT License - see [LICENSE](LICENSE) for details.

# Enterprise IT Ops Intelligence Platform

> **End-to-end AI platform** that predicts incident severity, detects cloud cost anomalies, forecasts SLA breaches, and enables natural language Q&A over operational data — built with Python, scikit-learn, PyTorch, LangChain, and Streamlit.

[![CI](https://github.com/YOUR_USERNAME/it-ops-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/it-ops-intelligence/actions)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 Project Overview

This platform simulates the kind of AI-powered operational intelligence system that enterprises like Kyndryl use to manage mission-critical infrastructure. It ingests data from 8 synthetic services (billing, auth, storage, ML inference, etc.) and applies a full ML + LLM pipeline to turn raw logs into actionable insights.

**Key capabilities:**

| Capability | Approach | Accuracy |
|---|---|---|
| Incident severity prediction (P1–P4) | RandomForest + XGBoost | ~85% weighted F1 |
| Cloud cost anomaly detection | Isolation Forest + Z-score + IQR | ~92% precision |
| SLA breach forecasting (14-day) | Prophet + PyTorch LSTM | MAE < 0.3% uptime |
| Natural language Q&A | LangChain RAG + FAISS + GPT-4o-mini | – |
| Executive dashboard | Streamlit + Plotly | – |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1 – Data Ingestion                                    │
│  Faker synthetic data → PostgreSQL → CSV (5,000+ incidents) │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 2 – ML Pipeline (MLflow tracked)                     │
│  • Severity Classifier   RandomForest / XGBoost             │
│  • Anomaly Detector      Isolation Forest                   │
│  • SLA Forecaster        Prophet + LSTM                     │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 3 – LLM + RAG                                        │
│  FAISS vector store → LangChain agent → OpenAI/Claude API   │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 4 – Dashboard & Deployment                           │
│  Streamlit UI  |  Power BI  |  Docker  |  AWS/GCP           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
it-ops-intelligence/
├── data/
│   ├── generate_data.py        # Synthetic data generator (Faker)
│   └── raw/                    # Generated CSVs (gitignored)
├── models/
│   ├── severity_classifier.py  # RandomForest + XGBoost severity model
│   ├── anomaly_detection.py    # Isolation Forest cost anomaly model
│   ├── sla_forecaster.py       # Prophet + LSTM SLA breach forecaster
│   ├── saved/                  # Serialized models (joblib)
│   └── plots/                  # Auto-generated visualizations
├── rag/
│   └── rag_agent.py            # LangChain RAG agent + FAISS index
├── dashboard/
│   └── app.py                  # Streamlit multi-tab dashboard
├── sql/
│   ├── schema.sql              # PostgreSQL schema + views
│   └── queries.sql             # 12 analytical SQL queries
├── notebooks/
│   └── eda_analysis.py         # Full EDA (run as Jupyter via Jupytext)
├── tests/
│   └── test_pipeline.py        # 15 unit + integration tests
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml      # App + PostgreSQL + MLflow
├── .github/
│   └── workflows/ci.yml        # GitHub Actions CI/CD
├── config.py                   # Central paths, constants, env vars
├── train_all.py                # One-shot full pipeline runner
├── convert_notebook.py         # .py → .ipynb Jupyter converter
├── Makefile                    # make install / data / train / dashboard
└── .env.example                # Environment variable template
```

---

## 🚀 Quick Start

### One command (recommended)

```bash
git clone https://github.com/YOUR_USERNAME/it-ops-intelligence.git
cd it-ops-intelligence
python -m venv venv && source venv/bin/activate
make all        # install → data → train → notebook → dashboard
```

### Step by step

```bash
make install    # pip install -r requirements.txt
make data       # generate 5,000+ synthetic incidents + costs + SLA logs
make train      # train all 3 ML models (tracked in MLflow)
make notebook   # convert EDA .py → Jupyter .ipynb
make powerbi    # export aggregated Excel sheets for Power BI
make dashboard  # launch Streamlit at localhost:8501
```

Run `make help` to see all available targets.

Open http://localhost:8501

### Option B — Docker (full stack with PostgreSQL + MLflow)

```bash
cd docker
export OPENAI_API_KEY=sk-...          # optional, enables AI chat
docker-compose up --build
```

Services:
- Streamlit dashboard → http://localhost:8501
- MLflow tracking     → http://localhost:5000
- PostgreSQL          → localhost:5432

### Option C — Load SQL schema

```bash
psql -U itops -d itops_db -f sql/schema.sql
psql -U itops -d itops_db -f sql/queries.sql
```

---

## 🤖 AI Chat Assistant

The RAG chatbot answers questions like:

> *"Which services have the highest SLA breach risk this week?"*  
> *"What was the average P1 resolution time for billing-api in Q3?"*  
> *"Are there any cost anomalies I should be aware of?"*  
> *"Predict severity for an after-hours security incident in auth-service affecting 10,000 users"*

**To enable:** Enter your OpenAI or Anthropic API key in the dashboard's AI Chat tab.

---

## 📊 Key Findings (from EDA notebook)

**Incident patterns**
- P1 + P2 incidents are 25% of volume but consume 70%+ of resolution effort
- After-hours P1 MTTR is **2.3× longer** than business-hours P1
- Change-induced incidents impact **40% more users** on average
- `impacted_users` and `category` are the strongest severity predictors

**Cloud costs**
- 3% of cost days flagged as anomalies by Isolation Forest
- Isolation Forest achieves higher precision than Z-score (fewer false positives)
- Compute costs dominate at ~55% of total spend across all services

**SLA performance**
- Services with >5 daily incidents show **3× higher breach rate**
- 14-day Prophet forecast achieves uptime MAE < 0.3%
- Two services consistently breach SLA — recommended for capacity review

---

## 🧪 Testing

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

Test coverage: data generation, feature engineering, anomaly detection, end-to-end smoke tests.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Data | Python, Pandas, NumPy, Faker, PostgreSQL |
| ML | Scikit-learn, XGBoost, PyTorch, Prophet |
| Experiment tracking | MLflow |
| LLM / RAG | LangChain, FAISS, OpenAI API, Anthropic API |
| Dashboard | Streamlit, Plotly |
| Deployment | Docker, docker-compose, GitHub Actions |
| Cloud-ready | AWS EC2 / GCP Cloud Run compatible |

---

## 📈 MLflow Experiments

Three tracked experiments:
- `severity_classification` — RF vs XGBoost comparison
- `cloud_cost_anomaly_detection` — IF vs Z-score vs IQR
- `sla_breach_forecasting` — per-service breach probability

View at http://localhost:5000 when running with Docker.

---

## 🗺️ Roadmap

- [ ] Real-time Kafka ingestion pipeline
- [ ] SHAP explainability for severity classifier
- [ ] Power BI report template (`.pbix`)
- [ ] AWS CDK deployment script
- [ ] Slack alert integration via LangChain tool

---

## 👤 Author

**[Your Name]**  
MS Computer Engineering, Texas A&M University  
Specialization: AI & Data Science  
[LinkedIn](https://linkedin.com/in/YOUR_PROFILE) · [GitHub](https://github.com/YOUR_USERNAME)

---

## 📄 License

MIT — see [LICENSE](LICENSE)

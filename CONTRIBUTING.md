# Contributing

Thank you for your interest in contributing to the Enterprise IT Ops Intelligence Platform.

## Development setup

```bash
git clone https://github.com/YOUR_USERNAME/it-ops-intelligence.git
cd it-ops-intelligence
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your API keys
make data              # generate synthetic datasets
make train             # train all models
```

## Project structure

| Directory | Purpose |
|---|---|
| `data/` | Data generation, DB loader, Power BI export |
| `models/` | ML training scripts (classifier, anomaly, forecaster) |
| `rag/` | LangChain RAG agent + FAISS vector store |
| `dashboard/` | Streamlit multi-tab app |
| `sql/` | PostgreSQL schema and analytical queries |
| `notebooks/` | EDA analysis (Jupytext `.py` → `.ipynb`) |
| `tests/` | Pytest unit + integration tests |
| `docker/` | Dockerfile + docker-compose for full stack |

## Code style

This project uses **black**, **isort**, and **flake8**.

```bash
make lint-fix   # auto-format
make lint       # check only (CI runs this)
```

Line length: 100. Python version: 3.11+.

## Running tests

```bash
make test        # full suite with coverage
make test-fast   # stop on first failure
```

All PRs must pass the full test suite and lint checks (enforced by GitHub Actions CI).

## Adding a new ML model

1. Create `models/your_model.py` following the pattern in `severity_classifier.py`
2. Add MLflow experiment tracking with `mlflow.set_experiment("your_experiment")`
3. Save the trained model with `joblib.dump` to `models/saved/`
4. Add tests in `tests/test_pipeline.py`
5. Register the model in `train_all.py`
6. Expose predictions in `rag/rag_agent.py` as a new `@tool`

## Submitting changes

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit with clear messages: `git commit -m "Add SHAP explainability to severity classifier"`
4. Push and open a Pull Request against `main`
5. Ensure CI passes before requesting review

## Roadmap items (good first issues)

- [ ] SHAP values for severity classifier explainability
- [ ] Real-time Kafka/Kinesis data ingestion
- [ ] AWS CDK deployment script
- [ ] Power BI `.pbix` template file
- [ ] Slack alerting tool in LangChain agent
- [ ] Multi-tenant support (per-customer data isolation)

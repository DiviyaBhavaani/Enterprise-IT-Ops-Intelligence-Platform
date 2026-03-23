# ══════════════════════════════════════════════════════════════════════════════
#  Makefile  –  Enterprise IT Ops Intelligence Platform
#  Usage: make <target>
# ══════════════════════════════════════════════════════════════════════════════

PYTHON     = python3
STREAMLIT  = streamlit
PYTEST     = pytest
PIP        = pip

.PHONY: help install data train rag dashboard docker test lint clean notebook all

# ── Default ───────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  Enterprise IT Ops Intelligence Platform"
	@echo "  ───────────────────────────────────────"
	@echo "  make install      Install all Python dependencies"
	@echo "  make data         Generate synthetic IT ops datasets"
	@echo "  make train        Train all ML models (classifier + anomaly + SLA)"
	@echo "  make rag          Build RAG vector index (needs OPENAI_API_KEY)"
	@echo "  make notebook     Convert EDA .py to Jupyter .ipynb"
	@echo "  make powerbi      Export aggregated tables for Power BI"
	@echo "  make dashboard    Launch Streamlit dashboard (localhost:8501)"
	@echo "  make docker       Start full stack via docker-compose"
	@echo "  make test         Run pytest test suite"
	@echo "  make lint         Run black + isort + flake8"
	@echo "  make clean        Remove generated data, models, and caches"
	@echo "  make all          Full pipeline: install → data → train → dashboard"
	@echo ""

# ── Install ───────────────────────────────────────────────────────────────────
install:
	$(PIP) install -r requirements.txt

# ── Data generation ───────────────────────────────────────────────────────────
data:
	$(PYTHON) data/generate_data.py

# ── Model training ────────────────────────────────────────────────────────────
train:
	$(PYTHON) train_all.py --skip-rag

# ── RAG index (requires API key) ──────────────────────────────────────────────
rag:
	@if [ -z "$$OPENAI_API_KEY" ] && [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "[ERROR] Set OPENAI_API_KEY or ANTHROPIC_API_KEY first."; \
		exit 1; \
	fi
	$(PYTHON) train_all.py --steps 5

# ── Notebook conversion ───────────────────────────────────────────────────────
notebook:
	$(PYTHON) convert_notebook.py

# ── Power BI export ───────────────────────────────────────────────────────────
powerbi:
	$(PYTHON) data/powerbi_export.py

# ── Dashboard ─────────────────────────────────────────────────────────────────
dashboard:
	$(STREAMLIT) run dashboard/app.py \
		--server.port 8501 \
		--server.headless false

# ── Docker full stack ─────────────────────────────────────────────────────────
docker:
	cd docker && docker-compose up --build

docker-down:
	cd docker && docker-compose down -v

# ── Database ──────────────────────────────────────────────────────────────────
db-load:
	$(PYTHON) data/db_loader.py --reset

# ── Testing ───────────────────────────────────────────────────────────────────
test:
	$(PYTEST) tests/ -v --tb=short --cov=. --cov-report=term-missing

test-fast:
	$(PYTEST) tests/ -v --tb=short -x

# ── Linting ───────────────────────────────────────────────────────────────────
lint:
	black  --check --diff .
	isort  --check-only --diff .
	flake8 . --max-line-length=100 --exclude=.git,__pycache__,notebooks,venv

lint-fix:
	black .
	isort .

# ── Full pipeline ─────────────────────────────────────────────────────────────
all: install data train notebook powerbi dashboard

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	@echo "Removing generated artefacts …"
	rm -rf data/raw/*.csv data/raw/*.parquet
	rm -rf models/saved/*.pkl models/saved/*.joblib
	rm -rf models/plots/*.png
	rm -rf rag/faiss_index/
	rm -rf mlruns/ mlartifacts/
	rm -rf __pycache__ **/__pycache__
	rm -rf .pytest_cache .coverage coverage.xml htmlcov/
	rm -rf notebooks/eda_analysis.ipynb
	@echo "Clean complete."

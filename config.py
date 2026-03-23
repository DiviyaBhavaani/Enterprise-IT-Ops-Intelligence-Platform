"""
config.py  –  Central configuration for the IT Ops Intelligence Platform
All paths, model params, and environment settings live here.
"""

import os
from pathlib import Path

# ── Project root ──────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.resolve()

# ── Data paths ────────────────────────────────────────────────────────────────
DATA_RAW            = ROOT / "data" / "raw"
INCIDENTS_CSV       = DATA_RAW / "incidents.csv"
CLOUD_COSTS_CSV     = DATA_RAW / "cloud_costs.csv"
SLA_LOGS_CSV        = DATA_RAW / "sla_logs.csv"
CLOUD_COSTS_SCORED  = DATA_RAW / "cloud_costs_scored.csv"
SLA_RISK_SUMMARY    = DATA_RAW / "sla_risk_summary.csv"

# ── Model paths ───────────────────────────────────────────────────────────────
MODELS_DIR          = ROOT / "models"
MODELS_SAVED        = MODELS_DIR / "saved"
MODELS_PLOTS        = MODELS_DIR / "plots"
SEVERITY_MODEL      = MODELS_SAVED / "severity_classifier.pkl"
ANOMALY_MODEL       = MODELS_SAVED / "anomaly_detector.pkl"
SLA_LSTM_MODEL      = MODELS_SAVED / "sla_lstm_bundle.pkl"

# ── RAG paths ─────────────────────────────────────────────────────────────────
RAG_DIR             = ROOT / "rag"
FAISS_INDEX         = RAG_DIR / "faiss_index"

# ── Database ──────────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://itops:itops_secret@localhost:5432/itops_db"
)

# ── MLflow ────────────────────────────────────────────────────────────────────
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")

# ── LLM API keys ──────────────────────────────────────────────────────────────
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY",    "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ── Data generation params ────────────────────────────────────────────────────
N_INCIDENTS   = 5_000
N_DAYS        = 365
RANDOM_STATE  = 42

SERVICES = [
    "auth-service", "billing-api", "data-pipeline",
    "ml-inference", "notification-svc", "storage-gateway",
    "identity-mgr", "reporting-engine",
]

SEVERITIES   = ["P1", "P2", "P3", "P4"]
SEV_WEIGHTS  = [0.05, 0.20, 0.45, 0.30]
CATEGORIES   = ["hardware", "network", "application",
                "security", "performance", "configuration"]
TEAMS        = ["infra", "devops", "security", "app-support", "cloud-ops"]

# ── ML params ─────────────────────────────────────────────────────────────────
FORECAST_DAYS         = 14
ANOMALY_CONTAMINATION = 0.03
SLA_TARGET_PCT        = 99.5

# ── Ensure dirs exist ─────────────────────────────────────────────────────────
for d in [DATA_RAW, MODELS_SAVED, MODELS_PLOTS, FAISS_INDEX]:
    d.mkdir(parents=True, exist_ok=True)

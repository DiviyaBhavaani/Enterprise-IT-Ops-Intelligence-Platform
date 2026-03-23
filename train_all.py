"""
train_all.py  –  Run the full training pipeline in one command.

Steps:
  1. Generate synthetic data (if CSVs missing)
  2. Train severity classifier   → models/saved/severity_classifier.pkl
  3. Train anomaly detector      → models/saved/anomaly_detector.pkl
  4. Train SLA forecaster        → models/saved/sla_lstm_bundle.pkl
  5. Build RAG vector index      → rag/faiss_index/

Usage:
    python train_all.py                  # full pipeline
    python train_all.py --skip-data      # skip data generation
    python train_all.py --skip-rag       # skip vector index build
    python train_all.py --steps 1,2,3   # run specific steps
"""

import os
import sys
import time
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def banner(step: int, title: str):
    print(f"\n{'='*64}")
    print(f"  Step {step}: {title}")
    print(f"{'='*64}")


def step_data():
    banner(1, "Generating synthetic IT ops data")
    from data.generate_data import generate_incidents, generate_cloud_costs, generate_sla_logs
    from config import INCIDENTS_CSV, CLOUD_COSTS_CSV, SLA_LOGS_CSV

    if all(os.path.exists(p) for p in [INCIDENTS_CSV, CLOUD_COSTS_CSV, SLA_LOGS_CSV]):
        print("  Data already exists – skipping generation.")
        print("  (Delete data/raw/*.csv to force regeneration)")
        return

    import os as _os
    os.makedirs("data/raw", exist_ok=True)

    t = time.time()
    inc = generate_incidents();  inc.to_csv(INCIDENTS_CSV,   index=False)
    cc  = generate_cloud_costs(); cc.to_csv(CLOUD_COSTS_CSV, index=False)
    sla = generate_sla_logs();   sla.to_csv(SLA_LOGS_CSV,    index=False)
    print(f"  Generated {len(inc):,} incidents, {len(cc):,} cost rows, "
          f"{len(sla):,} SLA rows in {time.time()-t:.1f}s")


def step_severity():
    banner(2, "Training severity classifier (RandomForest + XGBoost)")
    t = time.time()
    from models.severity_classifier import train
    train()
    print(f"  Done in {time.time()-t:.1f}s")


def step_anomaly():
    banner(3, "Training cloud cost anomaly detector (Isolation Forest)")
    t = time.time()
    from models.anomaly_detection import train
    train()
    print(f"  Done in {time.time()-t:.1f}s")


def step_sla():
    banner(4, "Training SLA breach forecaster (Prophet + LSTM)")
    t = time.time()
    from models.sla_forecaster import train
    train()
    print(f"  Done in {time.time()-t:.1f}s")


def step_rag(openai_key: str = "", anthropic_key: str = ""):
    banner(5, "Building RAG vector index (FAISS)")
    api_key = openai_key or os.getenv("OPENAI_API_KEY", "")
    ant_key = anthropic_key or os.getenv("ANTHROPIC_API_KEY", "")

    if not api_key and not ant_key:
        print("  [SKIP] No API key found.")
        print("  Set OPENAI_API_KEY or ANTHROPIC_API_KEY to build the vector index.")
        print("  The dashboard's AI chat will fall back to rule-based responses.")
        return

    t = time.time()
    from rag.rag_agent import build_agent
    build_agent(openai_key or None, anthropic_key or None, force_rebuild=True)
    print(f"  Done in {time.time()-t:.1f}s")


# ── Summary reporter ──────────────────────────────────────────────────────────
def print_summary():
    from config import (SEVERITY_MODEL, ANOMALY_MODEL, SLA_LSTM_MODEL,
                        FAISS_INDEX, SLA_RISK_SUMMARY)
    print(f"\n{'='*64}")
    print("  Pipeline summary")
    print(f"{'='*64}")

    checks = [
        ("Severity classifier",   SEVERITY_MODEL),
        ("Anomaly detector",      ANOMALY_MODEL),
        ("SLA LSTM bundle",       SLA_LSTM_MODEL),
        ("SLA risk summary CSV",  SLA_RISK_SUMMARY),
        ("RAG FAISS index",       FAISS_INDEX / "index.faiss"),
    ]
    all_ok = True
    for label, path in checks:
        ok = os.path.exists(path)
        if not ok:
            all_ok = False
        print(f"  {'✅' if ok else '❌'} {label}")

    print()
    if all_ok:
        print("  All artefacts built. Launch the dashboard:")
        print("    streamlit run dashboard/app.py")
    else:
        print("  Some artefacts missing (see above).")
        print("  Re-run: python train_all.py")
    print(f"{'='*64}\n")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Full IT Ops training pipeline")
    parser.add_argument("--skip-data",  action="store_true", help="Skip data generation")
    parser.add_argument("--skip-rag",   action="store_true", help="Skip RAG index build")
    parser.add_argument("--steps",      type=str, default="",
                        help="Comma-separated step numbers to run (e.g. 1,2,3)")
    parser.add_argument("--openai-key",    default="", help="OpenAI API key")
    parser.add_argument("--anthropic-key", default="", help="Anthropic API key")
    args = parser.parse_args()

    run_steps = set()
    if args.steps:
        run_steps = set(int(s.strip()) for s in args.steps.split(","))

    wall_start = time.time()
    errors     = []

    def run(step_num, fn, *fn_args):
        if run_steps and step_num not in run_steps:
            return
        try:
            fn(*fn_args)
        except Exception as e:
            errors.append((step_num, str(e)))
            print(f"\n  [ERROR] Step {step_num} failed: {e}")
            import traceback; traceback.print_exc()

    if not args.skip_data:
        run(1, step_data)
    run(2, step_severity)
    run(3, step_anomaly)
    run(4, step_sla)
    if not args.skip_rag:
        run(5, step_rag, args.openai_key, args.anthropic_key)

    total = time.time() - wall_start
    print(f"\nTotal pipeline time: {total/60:.1f} min")

    if errors:
        print(f"\n{len(errors)} step(s) had errors:")
        for step_num, msg in errors:
            print(f"  Step {step_num}: {msg}")

    print_summary()


if __name__ == "__main__":
    main()

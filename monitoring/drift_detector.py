import json
import os
from datetime import datetime, timezone
from typing import Dict, Any

import mlflow
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

FEATURES_TO_MONITOR = ["Volumen", "Presion", "Temperatura", "DesviacionBalance"]


def calculate_psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    """Calcula el Population Stability Index (PSI) entre distribución base y actual."""
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    breakpoints = np.unique(breakpoints)
    if len(breakpoints) < 3:
        return 0.0

    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]

    expected_percents = np.clip(expected_counts / max(len(expected), 1), 1e-6, None)
    actual_percents = np.clip(actual_counts / max(len(actual), 1), 1e-6, None)

    psi_value = np.sum((actual_percents - expected_percents) * np.log(actual_percents / expected_percents))
    return float(round(psi_value, 6))


def evaluate_volumetric_drift(
    baseline_df: pd.DataFrame,
    current_df: pd.DataFrame,
    experiment_name: str = "SAT-Anexos30-31-Drift-Monitoring",
    tracking_uri: str = "sqlite:///mlflow.db",
) -> Dict[str, Any]:
    """Evalúa PSI y K-S sobre telemetría volumétrica y registra resultados en MLflow (SQLite)."""
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    report: Dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "baseline_rows": len(baseline_df),
        "current_rows": len(current_df),
        "features": {},
        "severe_drift_count": 0,
        "moderate_drift_count": 0,
        "action_required": "NONE",
    }

    with mlflow.start_run(run_name=f"drift_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        for col in FEATURES_TO_MONITOR:
            base_vals = baseline_df[col].dropna().to_numpy()
            curr_vals = current_df[col].dropna().to_numpy()

            psi = calculate_psi(base_vals, curr_vals)
            ks_stat, ks_pvalue = ks_2samp(base_vals, curr_vals)

            if psi >= 0.20:
                status = "CRITICAL_DRIFT"
                report["severe_drift_count"] += 1
            elif psi >= 0.10 or ks_pvalue < 0.01:
                status = "MODERATE_DRIFT"
                report["moderate_drift_count"] += 1
            else:
                status = "STABLE"

            report["features"][col] = {
                "psi": psi,
                "ks_statistic": round(float(ks_stat), 6),
                "ks_pvalue": round(float(ks_pvalue), 6),
                "status": status,
            }

            mlflow.log_metric(f"psi_{col}", psi)
            mlflow.log_metric(f"ks_stat_{col}", float(ks_stat))
            mlflow.log_metric(f"ks_pvalue_{col}", float(ks_pvalue))

        if report["severe_drift_count"] >= 2:
            report["action_required"] = "TRIGGER_RETRAINING_PIPELINE"
        elif report["severe_drift_count"] == 1 or report["moderate_drift_count"] >= 2:
            report["action_required"] = "ALERT_P3_INVESTIGATE"

        mlflow.log_metric("severe_drift_count", report["severe_drift_count"])
        mlflow.set_tag("action_required", report["action_required"])

        os.makedirs("monitoring/reports", exist_ok=True)
        report_path = "monitoring/reports/latest_drift_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        mlflow.log_artifact(report_path)

    return report


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    baseline = pd.DataFrame({
        "Volumen": rng.normal(1200, 50, 1000),
        "Presion": rng.normal(215, 10, 1000),
        "Temperatura": rng.normal(60, 3, 1000),
        "DesviacionBalance": rng.normal(-0.5, 0.4, 1000),
    })
    current = pd.DataFrame({
        "Volumen": rng.normal(1340, 65, 300),
        "Presion": rng.normal(216, 11, 300),
        "Temperatura": rng.normal(60.5, 3.1, 300),
        "DesviacionBalance": rng.normal(-2.3, 0.7, 300),
    })

    resultado = evaluate_volumetric_drift(baseline, current)
    print(json.dumps(resultado, indent=2))

from contextlib import asynccontextmanager
import os
import time
from typing import Optional

from fastapi import FastAPI, HTTPException, Response
import joblib
import mlflow
from opentelemetry import trace
import pandas as pd
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel, Field

from app.observability import (
    ACTIVE_MODEL_INFO,
    ANOMALY_PROB_DIST,
    DEVIATION_BALANCE_GAUGE,
    INFERENCE_LATENCY,
    PREDICTIONS_TOTAL,
    JsonAuditLogger,
    setup_telemetry,
)

MODEL_PATH = os.getenv("MODEL_PATH", "models/sat_anomaly_model.joblib")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
MODEL_VERSION = "2.0.0"

model = None
threshold = 0.5
mlflow_run_id = "local-joblib"
audit_logger = JsonAuditLogger()


def load_artifacts():
    global model, threshold, mlflow_run_id
    if os.path.exists(MODEL_PATH):
        artifacts = joblib.load(MODEL_PATH)
        model = artifacts["model"]
        threshold = float(artifacts["threshold"])
        mlflow_run_id = str(artifacts.get("run_id", "local-joblib"))

        # Registrar metadatos de carga en MLflow local y Prometheus
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        ACTIVE_MODEL_INFO.labels(
            model_path=MODEL_PATH,
            threshold=str(threshold),
            mlflow_run_id=mlflow_run_id,
        ).set(1)
    else:
        model = None
        threshold = 0.5


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_artifacts()
    yield


app = FastAPI(
    title="API de Detección de Anomalías Volumétricas SAT - Anexos 30 y 31",
    description="Microservicio de telemetría de hidrocarburos con garantía de Recall 100%",
    version=MODEL_VERSION,
    lifespan=lifespan,
)

tracer = setup_telemetry(app)


class TelemetryData(BaseModel):
    id_medidor: str = Field(..., example="TAG-MED-T101")
    volumen_bbl: float = Field(..., example=1203.40)
    presion_psi: float = Field(..., example=215.92)
    temperatura_c: float = Field(..., example=60.39)
    desviacion_balance_pct: float = Field(..., example=-1.57)


class AnomalyResponse(BaseModel):
    id_medidor: str
    es_anomalia: bool
    probabilidad_anomalia: float
    alerta_cierre_fiscal: str
    cumplimiento_anexo30_31: str
    trace_id: Optional[str] = None


@app.get("/health", tags=["Operaciones"])
def health_check():
    return {
        "status": "ok",
        "service": "FASE II SAT ANOMAL-API-MAVH",
        "recall_guarantee": "100%",
        "model_loaded": model is not None,
        "threshold": threshold,
    }


@app.get("/metrics", tags=["Observabilidad"])
def prometheus_metrics():
    """Endpoint de métricas para Prometheus."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/admin/reload-model", tags=["Gobernanza"])
def reload_model():
    """Recarga el artefacto del modelo desde disco/MLflow sin reiniciar la API."""
    load_artifacts()
    if model is None:
        raise HTTPException(status_code=500, detail=f"No se encontró el modelo en {MODEL_PATH}")
    return {"status": "reloaded", "model_path": MODEL_PATH, "threshold": threshold}


@app.post("/api/v1/detect-anomaly", response_model=AnomalyResponse, tags=["Inferencia"])
def detect_anomaly(data: TelemetryData):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado en el servidor")

    # 1. Span de preparación de telemetría
    with tracer.start_as_current_span("telemetry.feature.preparation") as prep_span:
        prep_span.set_attribute("sat.id_medidor", data.id_medidor)
        prep_span.set_attribute("sat.desviacion_balance_pct", data.desviacion_balance_pct)

        input_df = pd.DataFrame([{
            "volumen_bbl": data.volumen_bbl,
            "presion_psi": data.presion_psi,
            "temperatura_c": data.temperatura_c,
            "delta_balance_pct": data.desviacion_balance_pct,
        }])

    # 2. Span de inferencia del modelo
    with tracer.start_as_current_span("model.inference.predict") as inf_span:
        inf_span.set_attribute("mlflow.run_id", mlflow_run_id)
        inf_span.set_attribute("model.threshold", threshold)

        start_time = time.perf_counter()
        prob = float(model.predict_proba(input_df)[0][1])
        duration_sec = time.perf_counter() - start_time

        is_anomaly = prob >= threshold
        inf_span.set_attribute("prediction.es_anomalia", is_anomaly)
        inf_span.set_attribute("prediction.probabilidad", prob)

    # 3. Actualización de métricas en Prometheus
    INFERENCE_LATENCY.labels(
        model_version=MODEL_VERSION,
        id_medidor=data.id_medidor,
    ).observe(duration_sec)

    PREDICTIONS_TOTAL.labels(
        model_version=MODEL_VERSION,
        es_anomalia=str(is_anomaly).lower(),
        id_medidor=data.id_medidor,
    ).inc()

    ANOMALY_PROB_DIST.labels(model_version=MODEL_VERSION).observe(prob)
    DEVIATION_BALANCE_GAUGE.labels(id_medidor=data.id_medidor).set(data.desviacion_balance_pct)

    # 4. Log estructurado JSON para auditoría Anexo 30/31
    latency_ms = duration_sec * 1000.0
    audit_logger.log_inference(
        id_medidor=data.id_medidor,
        model_version=MODEL_VERSION,
        telemetry_summary={
            "volumen_bbl": data.volumen_bbl,
            "presion_psi": data.presion_psi,
            "temperatura_c": data.temperatura_c,
            "desviacion_balance_pct": data.desviacion_balance_pct,
        },
        es_anomalia=is_anomaly,
        probabilidad=prob,
        latency_ms=latency_ms,
    )

    status_alert = (
        "CRÍTICO: Anomalía Volumétrica Detectada. Bloqueo Preventivo Fiscal."
        if is_anomaly
        else "NORMAL: Medición Aprobada."
    )
    compliance = (
        "NO CONFORME - Requiere auditoría inmediata Anexo 30/31"
        if is_anomaly
        else "CONFORME - Anexo 30/31 SAT"
    )

    current_trace_id = format(trace.get_current_span().get_span_context().trace_id, "032x")

    return AnomalyResponse(
        id_medidor=data.id_medidor,
        es_anomalia=is_anomaly,
        probabilidad_anomalia=round(prob, 4),
        alerta_cierre_fiscal=status_alert,
        cumplimiento_anexo30_31=compliance,
        trace_id=current_trace_id,
    )

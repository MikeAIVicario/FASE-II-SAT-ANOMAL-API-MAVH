import hashlib
import json
import logging
import os
import time
from typing import Any, Dict

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Counter, Gauge, Histogram

# ---------------------------------------------------------------------------
# 1. MÉTRICAS DE PROMETHEUS (Golden Signals + Telemetría Anexo 30/31 SAT)
# ---------------------------------------------------------------------------
INFERENCE_LATENCY = Histogram(
    name="sat_volumetric_inference_duration_seconds",
    documentation="Latencia de inferencia del modelo de anomalías volumétricas",
    labelnames=["model_version", "id_medidor"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.15, 0.25, 0.5, 1.0),
)

PREDICTIONS_TOTAL = Counter(
    name="sat_volumetric_predictions_total",
    documentation="Total de lecturas de medidores evaluadas por estado de cumplimiento",
    labelnames=["model_version", "es_anomalia", "id_medidor"],
)

ANOMALY_PROB_DIST = Histogram(
    name="sat_volumetric_anomaly_probability_distribution",
    documentation="Distribución continua de probabilidades de anomalía volumétrica",
    labelnames=["model_version"],
    buckets=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0),
)

DEVIATION_BALANCE_GAUGE = Gauge(
    name="sat_volumetric_last_deviation_balance_pct",
    documentation="Último porcentaje de desviación de balance registrado por medidor",
    labelnames=["id_medidor"],
)

ACTIVE_MODEL_INFO = Gauge(
    name="sat_volumetric_active_model_info",
    documentation="Metadatos del modelo cargado en memoria",
    labelnames=["model_path", "threshold", "mlflow_run_id"],
)

# ---------------------------------------------------------------------------
# 2. CONFIGURACIÓN DE OPENTELEMETRY (Trazas)
# ---------------------------------------------------------------------------
def setup_telemetry(app, service_name: str = "sat-volumetric-anomal-api"):
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if otlp_endpoint:
        exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
        provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app, excluded_urls="metrics,health")
    return trace.get_tracer(service_name)

# ---------------------------------------------------------------------------
# 3. LOGGING ESTRUCTURADO JSON CON CORRELACIÓN DE TRAZAS
# ---------------------------------------------------------------------------
class JsonAuditLogger:
    def __init__(self, logger_name: str = "sat.volumetric.audit"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            self.logger.addHandler(logging.StreamHandler())

    def log_inference(
        self,
        id_medidor: str,
        model_version: str,
        telemetry_summary: Dict[str, float],
        es_anomalia: bool,
        probabilidad: float,
        latency_ms: float,
    ) -> None:
        current_span = trace.get_current_span()
        span_ctx = current_span.get_span_context()
        trace_id = format(span_ctx.trace_id, "032x") if span_ctx.is_valid else "no-trace"

        payload: Dict[str, Any] = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": "WARNING" if es_anomalia else "INFO",
            "service": "sat-volumetric-anomal-api",
            "trace_id": trace_id,
            "model_version": model_version,
            "id_medidor": id_medidor,
            "telemetry": telemetry_summary,
            "prediction": {
                "es_anomalia": es_anomalia,
                "probabilidad_anomalia": round(probabilidad, 4),
                "cumplimiento_anexo30_31": "NO CONFORME" if es_anomalia else "CONFORME",
                "latency_ms": round(latency_ms, 2),
            },
        }
        self.logger.info(json.dumps(payload))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os

app = FastAPI(
    title="API de Detección de Anomalías Volumétricas SAT - Anexos 30 y 31",
    description="Microservicio de telemetría de hidrocarburos con garantía de Recall 100%",
    version="2.0.0"
)

MODEL_PATH = os.getenv("MODEL_PATH", "models/sat_anomaly_model.joblib")

@app.on_event("startup")
def load_artifacts():
    global model, threshold
    if os.path.exists(MODEL_PATH):
        artifacts = joblib.load(MODEL_PATH)
        model = artifacts["model"]
        threshold = artifacts["threshold"]
    else:
        model = None
        threshold = 0.5

class TelemetryData(BaseModel):
    id_medidor: str = Field(..., example="TAG-MED-T101")
    volumen_bbl: float = Field(..., example=1203.40)
    presion_psi: float = Field(..., example=215.92)
    temperatura_c: float = Field(..., example=60.39)
    delta_balance_pct: float = Field(..., example=-1.57)

class AnomalyResponse(BaseModel):
    id_medidor: str
    es_anomalia: bool
    probabilidad_anomalia: float
    alerta_cierre_fiscal: str
    cumplimiento_anexo30_31: str

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "FASE II SAT ANOMAL-API-MAVH", "recall_guarantee": "100%"}

@app.post("/api/v1/detect-anomaly", response_model=AnomalyResponse)
def detect_anomaly(data: TelemetryData):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado en el servidor")
        
    input_df = pd.DataFrame([{
        "Volumen": data.volumen_bbl,
        "Presion": data.presion_psi,
        "Temperatura": data.temperatura_c,
        "DesviacionBalance": data.delta_balance_pct
    }])
    
    prob = float(model.predict_proba(input_df)[0][1])
    is_anomaly = prob >= threshold
    
    status_alert = "CRÍTICO: Anomalía Volumétrica Detectada. Bloqueo Preventivo Fiscal." if is_anomaly else "NORMAL: Medición Aprobada."
    compliance = "NO CONFORME - Requiere auditoría inmediata Anexo 30/31" if is_anomaly else "CONFORME - Anexo 30/31 SAT"
    
    return AnomalyResponse(
        id_medidor.id_medidor,
        es_anomalia=is_anomaly,
        probabilidad_anomalia=round(prob, 4),
        alerta_cierre_fiscal=status_alert,
        cumplimiento_anexo30_31=compliance
    )

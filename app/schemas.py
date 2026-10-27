# Definición de esquemas adicionales Pydantic
from pydantic import BaseModel, Field
from typing import List, Optional

class TelemetryInput(BaseModel):
    id_medidor: str = Field(..., example="TAG-MED-T101", description="Identificador único del medidor")
    volumen_bbl: float = Field(..., example=1208.15, description="Volumen medido en barriles")
    presion_psi: float = Field(..., example=153.22, description="Presión en PSI")
    temperatura_c: float = Field(..., example=25.78, description="Temperatura en grados Celsius")
    delta_balance_pct: float = Field(..., example=0.13, description="Porcentaje de variación/desbalance")

class AnomalyPredictionOutput(BaseModel):
    id_medidor: str
    probabilidad_anomalia: float
    es_anomalia: bool
    umbral_aplicado: float
    dictamen_sat: str
    requiere_inspeccion_campo: bool

class BatchTelemetryInput(BaseModel):
    lecturas: List[TelemetryInput]

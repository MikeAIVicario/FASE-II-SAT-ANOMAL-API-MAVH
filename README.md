# FASE II SAT ANOMAL-API-MAVH

Solución técnica para la **Detección de Anomalías Volumétricas en Telemetría de Hidrocarburos** alineada a los Anexos 30 y 31 del SAT.

# Fase II SAT Anexo 30-31 anoma-api

API REST productiva desarrollada con FastAPI, Docker y Machine Learning para la **detección automática de anomalías volumétricas en la contabilidad de hidrocarburos**, en estricto cumplimiento con las especificaciones de los **Anexos 30 y 31 del SAT**.

## 📌 Características Clave
* **Nombre del Repositorio:** `Fase II SAT Anexo 30-31 anoma-api`
* **Modelo:** Random Forest Classifier optimizado.
* **Umbral de Decisión:** $t = 0.20$ (Garantiza **Recall = 100%** y **0 Falsos Negativos**).
* **Dataset de Entrenamiento:** `ACT6_dataset_anomalias_volumetricas_MAVH.csv`.

## 🚀 Instrucciones de Inicio Rápido (Local)

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/tu-usuario/fase-ii-sat-anexo-30-31-anoma-api.git](https://github.com/tu-usuario/fase-ii-sat-anexo-30-31-anoma-api.git)
cd fase-ii-sat-anexo-30-31-anoma-api



## Estructura del Proyecto
- `app/`: Código de la API RESTful (FastAPI).
- `models/`: Artefactos e hiperparámetros del modelo entrenado.
- `notebooks/`: Cuadernos de entrenamiento y validación de métricas (Recall 100%).
- `data/`: Datasets de telemetría.

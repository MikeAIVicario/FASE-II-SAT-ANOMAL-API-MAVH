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

###  Clonar el Repositorio
```bash
git clone [https://github.com/tu-usuario/fase-ii-sat-anexo-30-31-anoma-api.git](https://github.com/tu-usuario/fase-ii-sat-anexo-30-31-anoma-api.git)
cd fase-ii-sat-anexo-30-31-anoma-api

## Estructura del Proyecto
- `app/`: Código de la API RESTful (FastAPI).
- `models/`: Artefactos e hiperparámetros del modelo entrenado.
- `notebooks/`: Cuadernos de entrenamiento y validación de métricas (Recall 100%).
- `data/`: Datasets de telemetría.

FASE-II-SAT-ANOMAL-API-MAVH/
├── data/               # Datasets de entrenamiento y prueba
├── models/             # Modelos de ML serializados (.pkl, .joblib)
├── src/                # Scripts de preprocesamiento, análisis y entrenamiento
├── app/                # Código fuente de la API (endpoints, esquemas)
│   ├── main.py         # Punto de entrada de la aplicación
│   └── schemas.py      # Definición de modelos de entrada/salida (Pydantic)
├── tests/              # Pruebas unitarias e integración
├── .gitignore          # Archivos excluidos de Git
├── requirements.txt    # Lista de dependencias
└── README.md           # Documentación principal

### Puesta en Operación y Validación Operativa

Abre un navegador web (Google Chrome, Firefox o Edge).Ingresa a la URL oficial del entorno de producción:
https://fase-ii-sat-anomal-api-mavh.onrender.com/docs

Confirma la carga del encabezado principal: API de Detección de Anomalías Volumétricas SAT - Anexos 30 y 31 (Versión 2.0.0)

Verificación de Disponibilidad del Servicio (Health Check)
En el bloque interactivo, ubicar y hacer clic sobre la ruta HTTP GET /health.
Hacer clic en el botón Try it out ubicado en el extremo derecho.
Presionar el botón azul Execute.Verifica que en Server response devuelva el código HTTP 200 con la siguiente estructura JSON:
{
  "status": "ok",
  "service": "FASE II SAT ANOMAL-API-MAVH",
  "recall_guarantee": "100%"
}

Validación del Modelo de Inferencia y Dictamen SAT
Ubicar el bloque de petición HTTP POST /api/v1/detect-anomaly.
Hacer clic sobre la barra para desplegar sus parámetros.Presiona el botón Try it out (parte superior derecha del bloque del endpoint).
En el campo de texto Request body, reemplaza el contenido por la siguiente telemetría de prueba con desviación volumétrica:JSON
{
  "id_medidor": "TAG-MED-RENDER-01",
  "volumen_bbl": 2096.92,
  "presion_psi": 228.43,
  "temperatura_c": 72.12,
  "delta_balance_pct": -2.53
}

Prueba Externa desde Terminal
Para validar que la API acepta peticiones directas desde sistemas externos, ejecuta el siguiente comando en la terminal (Git Bash, PowerShell o Cloud Shell):
curl -X POST "https://fase-ii-sat-anomal-api-mavh.onrender.com/api/v1/detect-anomaly" \
     -H "Content-Type: application/json" \
     -d '{
       "id_medidor": "TAG-MED-RENDER-01",
       "volumen_bbl": 2096.92,
       "presion_psi": 228.43,
       "temperatura_c": 72.12,
       "delta_balance_pct": -2.53
     }'

## 🚀 Despliegue y Puesta en Operación en la Nube (Render.com)

El microservicio de detección de anomalías volumétricas (cumplimiento SAT Anexos 30 y 31) se encuentra desplegado y operativo en la nube mediante un contenedor Docker alojado en **Render.com**.

### 📌 Información del Entorno de Producción

* **URL Base de Producción:** `https://fase-ii-sat-anomal-api-mavh.onrender.com`
* **Documentación Interoperable (Swagger UI):** `https://fase-ii-sat-anomal-api-mavh.onrender.com/docs`
* **Arquitectura de Contenedores:** Docker (Python 3.11 + FastAPI + Scikit-Learn 1.6.1)
* **Garantía de Modelo:** 100% Recall para auditoría fiscal.

---

### 🛠️ Paso a Paso del Proceso de Despliegue en Render

1. **Configuración del Servicio Web:**
   * Se conectó el repositorio de GitHub `MikeAIVicario/FASE-II-SAT-ANOMAL-API-MAVH` a la plataforma Render.com.
   * Se configuró el entorno de ejecución en modo **Docker**, permitiendo a Render detectar automáticamente el `Dockerfile` del proyecto.
   * Se asignó la rama `main` para el despliegue continuo (*Auto-Deploy*).

2. **Sincronización de Cambios y CI/CD:**
   * Cada actualización enviada a la rama `main` mediante `git push origin main` activa una tarea automática de compilación (*Build*) y despliegue (*Deploy*) en Render.
   * Se alinearon las dependencias del contenedor y se corrigieron los esquemas Pydantic (`app/schemas.py`) para garantizar la correcta validación de entrada de variables volumétricas.

---

### 🧪 Verificación Operativa y Pruebas de Integración

#### 1. Verificación de Disponibilidad (Health Check)
Para comprobar el estado operativo de la instancia en la nube, envía una petición GET a la ruta `/health`:

```bash
curl [https://fase-ii-sat-anomal-api-mavh.onrender.com/health](https://fase-ii-sat-anomal-api-mavh.onrender.com/health)


Respuesta de confirmación (HTTP 200):
{
  "status": "ok",
  "service": "FASE II SAT ANOMAL-API-MAVH",
  "recall_guarantee": "100%"
}

Prueba de Inferencia y Dictamen SAT
Para validar el pipeline de detección de anomalías en producción, envía un payload con la telemetría del medidor:

curl -X POST "[https://fase-ii-sat-anomal-api-mavh.onrender.com/api/v1/detect-anomaly](https://fase-ii-sat-anomal-api-mavh.onrender.com/api/v1/detect-anomaly)" \
     -H "Content-Type: application/json" \
     -d '{
       "id_medidor": "TAG-MED-RENDER-01",
       "volumen_bbl": 2096.92,
       "presion_psi": 228.43,
       "temperatura_c": 72.12,
       "delta_balance_pct": -2.53
     }'


Dictamen fiscal devuelto (HTTP 200):
{
  "id_medidor": "TAG-MED-RENDER-01",
  "es_anomalia": true,
  "probabilidad_anomalia": 1.0,
  "alerta_cierre_fiscal": "CRÍTICO: Anomalía Volumétrica Detectada. Bloqueo Preventivo Fiscal.",
  "cumplimiento_anexo30_31": "NO CONFORME - Requiere auditoría inmediata Anexo 30/31"
}


Nota de Latencia en Capa Gratuita: Tras 15 minutos de inactividad, la instancia de Render entra en estado de reposo (spin down).
La primera petición enviada tras un periodo de inactividad despertará el contenedor en aproximadamente 30 a 50 segundos. Las solicitudes posteriores responderán con baja latencia.



Pruebas Funcionales, Casos Extremos y Validación Operativa
Este capítulo detalla la metodología de verificación, ejecución de pruebas de integración y evaluación de casos de borde (edge cases) para el microservicio de Detección de Anomalías Volumétricas SAT (cumplimiento Anexos 30 y 31) alojado en Render.com.

El objetivo primordial del plan de pruebas es garantizar:La resiliencia del middleware de validación (Pydantic) frente a cargas de datos malformadas.La certeza del modelo de Machine Learning ante fluctuaciones térmicas, picos de presión y variaciones severas en el balance volumétrico.El cumplimiento normativo estricto al mantener una garantía de 100% Recall en la captura de desviaciones superiores al umbral permitido del $0.5\%$ por el SAT.


Escenario 1: Operación Normal (Línea Base)
Objetivo: Confirmar que las variables en rangos estándar no generen falsas alarmas de cierre fiscal.

Payload JSON:

JSON
{
  "id_medidor": "T101",
  "volumen_bbl": 1198.9,
  "presion_psi": 148.0,
  "temperatura_c": 25.0,
  "delta_balance_pct": 0.05
}


Escenario 2: Anomalía Térmica / Presión Alta (Edge Case 1)
Objetivo: Evaluar la detección ante variaciones críticas de presión y temperatura que afectan la densidad del hidrocarburo.

Payload JSON:

JSON
{
  "id_medidor": "T101",
  "volumen_bbl": 2096.9,
  "presion_psi": 228.4,
  "temperatura_c": 72.1,
  "delta_balance_pct": -2.53
}
Resultado Esperado (HTTP 200):
"es_anomalia": true, emisión de alerta de bloqueo preventivo fiscal y estatus NO CONFORME.



Escenario 3: Pérdida Físicamente Imposible (Edge Case 2)
Objetivo: Validar la captura de fugas masivas o extracciones no autorizadas donde la pérdida excede el límite del $0.5\%$.Payload JSON:JSON{
  "id_medidor": "T101",
  "volumen_bbl": 619.7,
  "presion_psi": 271.1,
  "temperatura_c": 22.4,
  "delta_balance_pct": 3.98
}
Resultado Esperado (HTTP 200):

"es_anomalia": true, probabilidad máxima de anomalía (1.0) y solicitud de auditoría inmediata.


Escenario 4: Ruido Cercano al Umbral / Límite Fronterizo (Edge Case 3)
Objetivo: Comprobar la respuesta conservadora del modelo calibrado a $100\%$ Recall ante fluctuaciones límite.Payload JSON:JSON{
  "id_medidor": "T101",
  "volumen_bbl": 1250.1,
  "presion_psi": 125.2,
  "temperatura_c": 10.4,
  "delta_balance_pct": -1.89
}
Resultado Esperado (HTTP 200):

"es_anomalia": true, asegurando la detención preventiva ante cualquier desvío potencial.




---

## 📊 Monitorización, Observabilidad y Gobernanza Operativa (MLOps)

El microservicio implementa una arquitectura de **observabilidad moderna** basada en los tres pilares (Métricas, Logs y Trazas), alineada con el cumplimiento regulatorio de los **Anexos 30 y 31 del SAT** (controles volumétricos de hidrocarburos) y la garantía operativa de **Recall 100%**.

### 1. Arquitectura de Telemetría (`app/observability.py`)

* **Métricas en Tiempo Real (Prometheus - `GET /metrics`):**
  * `sat_volumetric_inference_duration_seconds`: Histograma de latencia de inferencia por versión de modelo e `id_medidor`.
  * `sat_volumetric_predictions_total`: Contador de evaluaciones segmentado por resultado (`es_anomalia`) y medidor.
  * `sat_volumetric_anomaly_probability_distribution`: Distribución continua de probabilidades emitidas por el clasificador.
  * `sat_volumetric_last_deviation_balance_pct`: Medidor instantáneo (*Gauge*) del porcentaje de desviación de balance por tanque/medidor.
  * `sat_volumetric_active_model_info`: Inventario en memoria del artefacto cargado, umbral (`threshold`) y `mlflow_run_id`.
* **Trazas Distribuidas (OpenTelemetry):**
  * Instrumentación automática de rutas FastAPI y *spans* granulares para `telemetry.feature.preparation` y `model.inference.predict`, exportables vía protocolo OTLP hacia **Jaeger** o **Grafana Tempo** mediante `OTEL_EXPORTER_OTLP_ENDPOINT`.
* **Logs Estructurados de Auditoría (JSON):**
  * Cada petición emite un registro JSON correlacionado mediante `trace_id` con el resumen de variables físicas (`volumen_bbl`, `presion_psi`, `temperatura_c`, `desviacion_balance_pct`) y el dictamen fiscal (`CONFORME` / `NO CONFORME`).

### 2. SLOs, Presupuestos de Error y Alertas Inteligentes (`monitoring/prometheus_alerts.yml`)

| Indicador (SLI) | Objetivo (SLO) | Error Budget (30 días) | Regla de Alerta Asociada | Severidad |
| :--- | :--- | :--- | :--- | :--- |
| **Disponibilidad del Servicio** | **99.9%** | **0.1%** (~43.2 min) | `SATVolumetricAPIServiceDown` / `SATVolumetricHighErrorBurnRateP1` (Burn Rate >= 14.4x) | **P1** (Crítica) |
| **Latencia de Inferencia** | **p99 < 150 ms** | **1.0%** de peticiones lentas | `SATVolumetricHighLatencyP99` (sostenida > 10 min) | **P2** (Alta) |
| **Cumplimiento Volumétrico** | **Desviación <= ±2.0%** | **0.0%** (Tolerancia cero fiscal) | `SATVolumetricBalanceDeviationExceeded` | **P1** (Crítica) |
| **Estabilidad de Predicciones** | **Tasa anomalías <= 15%** | **1.5%** ventanas horarias | `SATVolumetricAnomalySpike` | **P2** (Alta) |

El enrutamiento de notificaciones se gestiona en `monitoring/alertmanager.yml` mediante variables de entorno (`${PAGERDUTY_WEBHOOK_URL}` y `${SLACK_WEBHOOK_URL}`).

### 3. Dashboards Operativos

La visualización en tiempo real se estructura en tres vistas operativas (Grafana + MLflow):
1. **Salud del Servicio y SLOs:** Consumo en tiempo real del *Error Budget*, *Burn Rate* horario y percentiles de latencia (p50, p95, p99).
2. **Observabilidad del Modelo ML:** Evolución de la tasa de anomalías detectadas, histograma de probabilidades frente a la línea base de entrenamiento y versión activa (`@champion`).
3. **Telemetría Física por Medidor:** Series temporales de `DesviacionBalance` y conteo de bloqueos preventivos fiscales por `id_medidor`.

### 4. Detección de Data Drift y Respuesta Automatizada (`monitoring/drift_detector.py`)

El pipeline de monitoreo evalúa periódicamente la deriva estadística sobre las cuatro variables físicas críticas (`Volumen`, `Presion`, `Temperatura`, `DesviacionBalance`) registrando métricas y artefactos (`monitoring/reports/latest_drift_report.json`) en **MLflow** (`sqlite:///mlflow.db`):

* **Population Stability Index (PSI):**
  * `PSI < 0.10`: Distribución estable (`STABLE`).
  * `0.10 <= PSI < 0.20` o `p-value K-S < 0.01`: Deriva moderada (`ALERT_P3_INVESTIGATE`).
  * `PSI >= 0.20` en 2 o más variables: Deriva severa (`TRIGGER_RETRAINING_PIPELINE`).
* **Flujos de Auto-Remediation:**
  * **Rollback en Caliente (`POST /admin/reload-model`):** Permite revertir el modelo en memoria a una versión estable previa sin reiniciar el contenedor ni perder disponibilidad.
  * **Reentrenamiento Continuo (CT):** Disparado automáticamente cuando `action_required == "TRIGGER_RETRAINING_PIPELINE"`, validando que el modelo candidato mantenga **Recall 100%** antes de su promoción.

### 5. Runbooks de Respuesta a Incidentes

#### <a id="runbook-01"></a>Runbook 01: Degradación de Latencia (p99 > 150 ms) o Burn Rate P1
1. **Diagnóstico:** Consultar trazas en Jaeger/Tempo filtrando por `duration > 150ms` para aislar si el cuello de botella ocurre en `telemetry.feature.preparation` o en `model.inference.predict`. Revisar saturación de CPU/RAM.
2. **Mitigación:** Escalar horizontalmente las réplicas del contenedor de la API (`docker compose up -d --scale api=3` o `kubectl scale`) y verificar tamaño de lote de peticiones entrantes.

#### <a id="runbook-02"></a>Runbook 02: Alerta de Desviación Volumétrica (> 2%) o Pico de Anomalías (> 15%)
1. **Diagnóstico:** Inspeccionar los logs JSON filtrando por `level: "WARNING"` e `id_medidor`. Ejecutar `python monitoring/drift_detector.py` para verificar si existe descalibración física en los sensores de presión/temperatura o un cambio brusco de distribución.
2. **Mitigación:**
   * Si es **desviación física confirmada**: Mantener el bloqueo preventivo fiscal del medidor afectado y notificar al área de Metrología/Auditoría Anexo 30 y 31.
   * Si es **corrupción en la ingesta de telemetría**: Activar protocolo de validación manual y revertir a la última versión estable del modelo mediante `POST /admin/reload-model`.

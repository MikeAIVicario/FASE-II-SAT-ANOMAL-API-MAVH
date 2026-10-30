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



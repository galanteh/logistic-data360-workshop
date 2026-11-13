# 🚚 LogisticForce: Salesforce Data Cloud (Data 360) Workshop

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Salesforce](https://img.shields.io/badge/Salesforce-00A1E0?style=for-the-badge&logo=salesforce&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)

Este repositorio contiene el código fuente, scripts de integración y materiales de un taller interactivo (Hands-On) diseñado para dominar la arquitectura E2E de **Salesforce Data Cloud (Data 360)**, aplicado a un caso de uso real en la industria logística (LogisticForce).

La interfaz proporciona una guía paso a paso, limpia y modular, donde los participantes construyen un motor de unificación de datos, analítica y alertas en tiempo real desde cero.

## 🚀 Rutas de Aprendizaje (Tracks)

El taller está dividido en dos modalidades para adaptarse al perfil de la audiencia:

### ⏱ Modo Especialista (3h) — Fundamentos E2E
Cubre el ciclo de vida fundacional de los datos logísticos:
1. **Ingesta y Armonización (DMOs):** Mapeo de objetos del Data Lake (DLOs) hacia el modelo canónico estándar, adaptando campos personalizados (ej. RFC).
2. **Identity Resolution:** Creación de reglas exactas y difusas (Fuzzy) para consolidar perfiles B2B fragmentados.
3. **Calculated Insights:** Creación de métricas (Volumetría y SLAs) usando enfoques SQL nativo y el Visual Builder.
4. **Segmentación Dinámica:** Cruce de métricas transaccionales e incidencias para detectar clientes en riesgo.
5. **Activación al CRM:** Configuración de Data Action Targets nativos para empujar segmentos hacia Salesforce Core.

### 🔬 Modo Arquitecto (5h) — Deep Dive & Real-Time
Desbloquea integraciones avanzadas y respuestas en sub-segundos:
* **6. Batch Data Transforms:** Enriquecimiento visual de datos (ej. derivación de Zonas Logísticas mediante nodos de fórmula).
* **7. Data Graphs:** Construcción visual y pre-materialización de JSONs profundos para historial 360 en <100ms.
* **8. Data Actions:** Monitoreo en tiempo real de registros para disparar *Platform Events* ante incidencias críticas.
* **9. Salesforce Flows:** Captura proactiva de eventos en el CRM para generar tareas operativas automáticas (Push & Pull).
* **10. Ingestion API (Streaming):** Arquitectura *headless* con Python usando OAuth 2.0 (JWT Bearer) para inyectar escaneos de paquetes en tiempo real al Data Lake.

## 📂 Estructura del Proyecto

```text
logistic-data360-workshop/
├── data/
│   ├── cuentas_b2b_logistica.csv      # Mock B2B con duplicados intencionales (Identity Res)
│   ├── guias_shipments_logistica.csv  # 50k registros transaccionales
│   ├── incidencias_entrega.csv        # Eventos operacionales para métricas de riesgo
│   └── log_cedis_scans.yaml           # Esquema OpenAPI 3.0 para la Ingestion API
├── downloads/
│   └── streaming_cedis.py             # Script Python (JWT Token Exchange) para Módulo 10
├── images/                            # Assets, diagramas y evidencias del paso a paso
├── index.html                         # Interfaz interactiva SPA del taller
├── generar_mock_data.py               # Generador Python para regenerar/ampliar datos
├── requirements.txt                   # Dependencias Python
├── composer.json                      # Configuración de Buildpack para Heroku
└── index.php                          # Enrutador estático para Heroku
```

## 💻 Ejecución Local

Para visualizar el taller o ejecutar las integraciones locales:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/logistic-data360-workshop.git
   cd logistic-data360-workshop
   ```
2. Para visualizar la guía, simplemente abre `index.html` en cualquier navegador.

**Para ejecutar el Streaming de Ingestion API (Módulo 10):**
```bash
# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias criptográficas y de red
pip install PyJWT requests cryptography

# Ejecutar el script (requiere configurar Consumer Key y private_key.pem previos)
python3 downloads/streaming_cedis.py
```

## ☁️ Despliegue en Heroku

El frontend interactivo está configurado para desplegarse fácilmente en Heroku utilizando el buildpack de PHP.

1. Inicia sesión en Heroku CLI:
   ```bash
   heroku login
   ```
2. Crea la aplicación:
   ```bash
   heroku apps:create logistic-data360-workshop
   ```
3. Despliega el código:
   ```bash
   git push heroku main
   heroku open
   ```

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

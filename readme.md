# 🚚 LogisticForce: Salesforce Data Cloud (Data 360) Workshop

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

Este repositorio contiene el código fuente y los materiales de un taller interactivo y práctico (Hands-On) diseñado para dominar los fundamentos de **Salesforce Data Cloud (Data 360)** aplicados a un caso de uso real en la industria logística.

La interfaz proporciona una guía paso a paso, limpia y elegante, para que los participantes construyan la arquitectura de datos desde cero.

## 🚀 Objetivos del Taller

El taller está dividido en tres ejercicios principales que cubren el ciclo de vida completo de los datos dentro de la plataforma:

1. **Ingesta y Armonización (DMOs):** Configuración de flujos de datos (Data Streams), mapeo de objetos del Data Lake (DLOs) hacia el modelo canónico estándar (Data Model Objects) adaptando campos personalizados (ej. RFC).
2. **Identity Resolution:** Creación de reglas de coincidencia (Matching Rules) exactas y difusas (Fuzzy) para unificar perfiles B2B fragmentados en un Perfil Unificado.
3. **Calculated Insights:** Creación de métricas multidimensionales utilizando dos enfoques arquitectónicos recomendados:
   - **Enfoque SQL (Zero JOINs):** Cálculo de Volumetría y SLAs consultando directamente las tablas de hechos para máxima eficiencia.
   - **Enfoque No-Code (Visual Builder):** Configuración visual de filtros y agrupaciones para monitorear incidencias operativas activas.

## 📂 Estructura del Proyecto

```text
logistic-data360-workshop/
├── data/                      # Archivos CSV de muestra (Mock Data) para el taller
├── images/                    # Capturas de pantalla y diagramas utilizados en la UI
├── index.html                 # Interfaz principal del taller y paso a paso
├── generar_mock_data.py       # Script en Python para regenerar datos de prueba
├── requirements.txt           # Dependencias del script de Python
├── composer.json              # Archivo de configuración (Trick para Heroku)
└── index.php                  # Enrutador estático para el despliegue en Heroku
```

## 💻 Ejecución Local

Para visualizar el taller en tu máquina local, no necesitas configuraciones complejas:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/logistic-data360-workshop.git
   ```
2. Navega a la carpeta del proyecto:
   ```bash
   cd logistic-data360-workshop
   ```
3. Simplemente abre el archivo `index.html` en tu navegador web favorito (Chrome, Firefox, Safari).

*(Opcional)* Si deseas ejecutar el generador de datos:
```bash
pip install -r requirements.txt
python generar_mock_data.py
```

## ☁️ Despliegue en Heroku

Este proyecto es estático (HTML/CSS/JS), pero está configurado para desplegarse fácilmente en Heroku utilizando el buildpack de PHP (a través de `composer.json` y `index.php`).

1. Inicia sesión en Heroku CLI:
   ```bash
   heroku login
   ```
2. Crea una nueva aplicación (opcionalmente dentro de un equipo):
   ```bash
   heroku apps:create nombre-de-tu-app --team nombre-del-equipo
   ```
3. Empuja el código al servidor de Heroku:
   ```bash
   git push heroku main
   ```
4. Abre la aplicación en vivo:
   ```bash
   heroku open
   ```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
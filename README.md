# Global Insights

Dashboard web interactivo para comparar indicadores económicos y sociales entre países utilizando datos oficiales de la **World Bank API**.

## Integrantes

- Aaron Vargas
- Adrián Gonzalez
- Ana María Ramírez
- Kristhel Porras

## Descripción del proyecto

Global Insights es una aplicación web que permite comparar el desempeño de dos países mediante indicadores internacionales como:

- Población.
- Producto Interno Bruto (PIB).
- PIB per cápita.
- Esperanza de vida.

La aplicación consume información desde una API externa, procesa los datos y los presenta mediante un dashboard visual orientado al análisis comparativo.

El objetivo del proyecto es demostrar la integración de una aplicación web con servicios externos, aplicando buenas prácticas de desarrollo y separación de responsabilidades.

---

# Problema que resuelve

Los usuarios que desean comparar países normalmente deben buscar información en diferentes fuentes y realizar comparaciones manualmente.

Global Insights centraliza esta información en una sola interfaz permitiendo:

- Consultar países disponibles.
- Comparar indicadores relevantes.
- Visualizar diferencias entre países.
- Facilitar la interpretación de datos internacionales.

---

# Usuario objetivo

El producto está orientado a:

- Estudiantes.
- Investigadores.
- Analistas de datos.
- Personas interesadas en economía internacional.
- Usuarios que desean comparar países mediante datos oficiales.

---

# Arquitectura del sistema

La arquitectura se mantiene deliberadamente pequeña: rutas HTTP, un servicio
de aplicación y un cliente para la API externa. Consulta
[`EXPLICACION.md`](EXPLICACION.md) para una guía breve de SOLID, DevOps y SecOps.

```
Global Insights

        Usuario
           |
           |
     Frontend Web
   HTML + CSS + JavaScript
           |
           |
        Flask API
           |
           |
    World Bank API
```

---

# Tecnologías utilizadas

## Backend

- Python.
- Flask.
- Requests.
- Flask-CORS.

Responsabilidades:

- Exponer endpoints.
- Consumir la API del Banco Mundial.
- Procesar respuestas JSON.
- Entregar datos al frontend.

---

## Frontend

- HTML5.
- CSS3.
- JavaScript.
- Chart.js.
- Bootstrap Icons.

Responsabilidades:

- Crear la interfaz del dashboard.
- Consultar el backend.
- Mostrar información dinámica.
- Generar visualizaciones.

---

# API utilizada

## World Bank API

Fuente:

World Bank Open Data API

Documentación:
https://data.worldbank.org/

La aplicación utiliza endpoints públicos sin necesidad de autenticación.

---

# Indicadores utilizados

| Indicador | Código World Bank |
|---|---|
| Población total | SP.POP.TOTL |
| Producto Interno Bruto | NY.GDP.MKTP.CD |
| PIB per cápita | NY.GDP.PCAP.CD |
| Esperanza de vida | SP.DYN.LE00.IN |

---

# Estructura del proyecto

```
global-insights/

│
├── backend/
│
│   ├── config.py
│   ├── app.py
│   ├── services.py
│   ├── world_bank.py
│   ├── requirements.txt
│
│
├── public/
│
│   ├── index.html
│   │
│   ├── css/
│   │     └── styles.css
│   │
│   └── js/
│         └── app.js
├── app.py              # Entrada de Vercel
├── requirements.txt    # Dependencias detectadas por Vercel
├── vercel.json
├── Dockerfile
└── README.md
```

---

# Instalación y ejecución

## 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
```

---

# Backend

Ejecutar los siguientes comandos desde la raíz del proyecto.

Crear entorno virtual:

```bash
python -m venv .venv
```

Activar entorno:

### Mac/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r backend/requirements-dev.txt
```

Ejecutar servidor desde la raíz del proyecto:

```bash
python -m backend.app
```

El backend estará disponible en:

```
http://127.0.0.1:5000
```

---

# Frontend

Abrir la carpeta:

```
public
```

Para reproducir localmente el entorno de producción, utilice `vercel dev` o
`docker compose up --build`. Los archivos estáticos están en `public/`.

Ejecutar `index.html` directamente no permite que las rutas relativas de la API
sean redirigidas al backend.

---

# Endpoints disponibles

## Obtener países

```
GET /countries
```

Ejemplo:

```
http://127.0.0.1:5000/countries
```

Respuesta:

```json
[
    {
        "id":"CRI",
        "name":"Costa Rica"
    }
]
```

---

## Comparar países

```
GET /compare?country1=CRI&country2=USA
```

Ejemplo:

```
http://127.0.0.1:5000/compare?country1=CRI&country2=USA
```

Respuesta:

```json
{
    "country1":{
        "country":"Costa Rica",
        "population":{
            "year":"2024",
            "value":5180000
        }
    },

    "country2":{
        "country":"United States"
    }
}
```

---

# Buenas prácticas aplicadas

✔ Separación frontend/backend.
✔ Módulo independiente para consumo de API externa.
✔ Manejo de errores tipados en solicitudes HTTP.
✔ Validación de respuestas.
✔ Uso de variables constantes.
✔ Código organizado por responsabilidades.
✔ Uso de JSON como formato de comunicación.
✔ Inyección de dependencias mediante un gateway.
✔ Configuración mediante variables de entorno.
✔ Pruebas unitarias, linting y análisis de seguridad en CI.

---

# Calidad, seguridad y operaciones

Ejecutar los controles locales desde la raíz del proyecto:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements-dev.txt
ruff check .
pytest
bandit --configfile pyproject.toml --recursive backend
pip-audit --requirement backend/requirements.txt
```

La configuración disponible está documentada en `.env.example`. No se deben
guardar archivos `.env`, credenciales ni entornos virtuales en el repositorio.

Para iniciar ambos servicios en contenedores:

```bash
docker compose up --build
```

Frontend: `http://127.0.0.1:8080`
API: `http://127.0.0.1:5000`

La imagen del backend se ejecuta con un usuario sin privilegios. Compose limita
capacidades, monta el filesystem como solo lectura y publica los puertos
únicamente en localhost. El workflow de CI ejecuta pruebas, lint, Bandit,
auditoría de dependencias y construcción de la imagen.

---

# Variables de entorno

La aplicación consume una API pública y no requiere API keys ni credenciales.
Las variables disponibles se documentan en `.env.example`:

| Variable | Descripción | Valor de ejemplo |
|---|---|---|
| `WORLD_BANK_BASE_URL` | URL base de la API del Banco Mundial | `https://api.worldbank.org/v2` |
| `WORLD_BANK_TIMEOUT` | Tiempo máximo de espera por solicitud, en segundos | `10` |

Para utilizar valores diferentes, crear un archivo `.env` local. Este archivo
está excluido mediante `.gitignore` y nunca debe subirse al repositorio.

---

# Uso de Supabase

Supabase no se utiliza porque Global Insights no necesita almacenar usuarios,
consultas ni historiales. Los indicadores se consultan en tiempo real desde la
API pública del Banco Mundial. Evitar una base de datos innecesaria mantiene la
solución sencilla y reduce su superficie de ataque.

---

# Buenas prácticas de DevOps y SecOps

## DevOps

- Dependencias de producción y desarrollo declaradas por separado.
- Pruebas, linting y controles de seguridad automatizados con GitHub Actions.
- Configuración diferenciada para ejecución local, Docker y Vercel.
- Endpoint `/health` para verificar la disponibilidad del backend.
- Imagen Docker reproducible y ejecución sin usuario root.
- Dependabot configurado para proponer actualizaciones.

## SecOps

- Archivos `.env`, entornos virtuales y archivos temporales excluidos de Git.
- Configuración externa mediante variables de entorno.
- Validación de códigos de país en el backend.
- Timeout y validación de las respuestas de la API externa.
- Mensajes de error públicos controlados; los detalles técnicos quedan en logs.
- Frontend construido con `textContent`, sin insertar HTML recibido externamente.
- Contenedores con filesystem de solo lectura y capacidades restringidas.
- Recomendaciones de seguridad de Vercel y Supabase revisadas.

---

# Producción

La aplicación está preparada para desplegarse como una Flask Function en
Vercel. El enlace público se agregará aquí después del primer despliegue:

**Vercel:** pendiente de despliegue.

---

# Posibles mejoras futuras

- Agregar histórico de indicadores.
- Incorporar más gráficos.
- Guardar consultas realizadas.
- Crear usuarios y perfiles.
- Implementar filtros por regiones.
- Incorporar más fuentes de datos internacionales.

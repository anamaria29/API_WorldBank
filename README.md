# Global Insights

Dashboard web interactivo para comparar indicadores económicos y sociales entre países utilizando datos oficiales de la **World Bank API**.

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
│   ├── app.py
│   ├── world_bank.py
│   ├── requirements.txt
│
│
├── frontend/
│
│   ├── index.html
│   │
│   ├── css/
│   │     └── styles.css
│   │
│   └── js/
│         └── app.js
│
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

Entrar a la carpeta:

```bash
cd backend
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno:

### Mac/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar servidor:

```bash
python app.py
```

El backend estará disponible en:

```
http://127.0.0.1:5000
```

---

# Frontend

Abrir la carpeta:

```
frontend
```

Ejecutar `index.html` mediante:

- Live Server de VS Code.
- O un servidor web local.

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
✔ Manejo de errores en solicitudes HTTP.  
✔ Validación de respuestas.  
✔ Uso de variables constantes.  
✔ Código organizado por responsabilidades.  
✔ Uso de JSON como formato de comunicación.  

---

# Posibles mejoras futuras

- Agregar histórico de indicadores.
- Incorporar más gráficos.
- Guardar consultas realizadas.
- Crear usuarios y perfiles.
- Implementar filtros por regiones.
- Agregar modo oscuro.
- Incorporar más fuentes de datos internacionales.


# 📄 Licencia

Proyecto académico desarrollado con fines educativos.

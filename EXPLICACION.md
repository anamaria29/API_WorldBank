# Guía corta para explicar el proyecto

## La idea en una frase

La aplicación recibe dos países, consulta datos del Banco Mundial y devuelve
una comparación. Cada parte tiene una sola responsabilidad y los errores se
manejan sin exponer detalles internos.

## Arquitectura: solo tres piezas

```text
Frontend → app.py → CountryComparisonService → WorldBankClient → World Bank API
             HTTP          caso de uso             integración externa
```

1. `app.py` se ocupa únicamente de HTTP: recibe parámetros, los valida y
   devuelve respuestas JSON con el código de estado correcto.
2. `services.py` contiene el caso de uso: coordina la comparación de países.
3. `world_bank.py` sabe comunicarse con el proveedor externo y transformar su
   respuesta.

No se agregaron repositorios, bases de datos, múltiples patrones ni capas que
el proyecto todavía no necesita.

## Cómo explicar SOLID

- **S — Responsabilidad única:** rutas, caso de uso y acceso externo están
  separados.
- **O — Abierto/cerrado:** se agregan indicadores modificando `INDICATORS`, sin
  reescribir el flujo de comparación.
- **L — Sustitución:** un cliente falso puede reemplazar al cliente real en las
  pruebas sin cambiar el servicio.
- **I — Interfaces pequeñas:** `WorldBankGateway` solo exige las dos operaciones
  que el servicio necesita.
- **D — Inversión de dependencias:** el servicio conoce el contrato
  `WorldBankGateway`, no conoce Flask ni `requests`.

La inyección ocurre en `create_app`: allí se conectan las piezas reales. En las
pruebas se conecta un `FakeGateway`, por lo que no se llama a internet.

## Buenas prácticas importantes

- Timeout para no dejar solicitudes bloqueadas.
- Validación de códigos de país antes de consultar el proveedor.
- Excepciones específicas y estados HTTP `400`, `404`, `502` y `500`.
- Mensajes públicos controlados; el detalle técnico queda en logs.
- Configuración mediante variables de entorno.
- DOM creado con `textContent`, evitando insertar HTML recibido de una API.
- Pruebas para rutas, validación, fallos externos y transformación de datos.

## DevOps, explicado de forma sencilla

El pipeline de `.github/workflows/ci.yml` hace cuatro preguntas en cada cambio:

1. ¿El código tiene problemas de estilo? — `ruff`.
2. ¿Las pruebas pasan? — `pytest`.
3. ¿Hay patrones inseguros? — `bandit`.
4. ¿Alguna dependencia tiene vulnerabilidades conocidas? — `pip-audit`.

Después construye la imagen Docker para comprobar que el despliegue sigue
siendo reproducible. Dependabot propone actualizaciones periódicas.

## SecOps, explicado de forma sencilla

La seguridad se aplica desde el desarrollo y no al final:

- El código y las dependencias se analizan en CI.
- Los secretos y archivos `.env` se excluyen del repositorio.
- Los contenedores no se ejecutan como root y pierden capacidades del sistema.
- El filesystem de los contenedores es de solo lectura.
- Frontend y API comparten origen, evitando abrir CORS innecesariamente.
- La API agrega headers de seguridad y no muestra excepciones internas.

## Demostración sugerida

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements-dev.txt
ruff check .
pytest
docker compose up --build
```

Probar después:

```bash
curl http://127.0.0.1:5000/health
curl "http://127.0.0.1:5000/compare?country1=CRI&country2=USA"
```

## Despliegue en Vercel

- `app.py` en la raíz es el punto de entrada que Vercel detecta.
- `requirements.txt` declara las dependencias que instala Vercel.
- `public/` contiene HTML, CSS y JavaScript servidos por el CDN.
- El frontend usa rutas relativas, por lo que no contiene una URL distinta para
  desarrollo y producción.
- `.python-version` mantiene Python 3.12 en local y producción.

Para simular el entorno antes de desplegar:

```bash
vercel dev
```

Cada push al repositorio conectado generará después un despliegue nuevo.

La explicación completa puede resumirse así: **pocas capas, dependencias
invertidas, errores controlados y controles automáticos antes de desplegar**.

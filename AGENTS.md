# Repository Guidelines

## Estructura del Proyecto y Organización de Módulos

- Mantén el código de aplicación dentro de `app/`. `main.py` expone la instancia de FastAPI; agrega paquetes como `routers/` para endpoints, `schemas/` para modelos Pydantic, `models/` para entidades ORM y `services/` para la lógica de negocio. Si surge infraestructura compartida, ubícala en `app/core/`.
- Replica la estructura en `tests/` (por ejemplo, `tests/routers/test_plan.py`) y centraliza fixtures comunes en `tests/conftest.py`.
- Gestiona dependencias Python en `requirements.txt`; fija versiones al incorporar librerías nuevas para asegurar despliegues reproducibles.

## Comandos de Build, Test y Desarrollo

- `python -m venv .venv && source .venv/bin/activate`: crea y activa el entorno virtual local.
- `pip install -r requirements.txt`: instala las dependencias de la aplicación.
- `uvicorn app.main:app --reload`: inicia la API en desarrollo con recarga automática en <http://localhost:8000>.
- `pytest`: ejecuta toda la batería de pruebas; usa `pytest tests/routers/test_plan.py -k plan` para validar casos puntuales.

## Estilo de Código y Convenciones de Nombres

- Sigue PEP 8 con indentación de 4 espacios y `snake_case` para módulos, funciones y variables; reserva `PascalCase` para esquemas Pydantic y clases ORM, y respeta un máximo de 88 caracteres por línea para alinear con flake8 y black.
- Prefiere imports absolutos explícitos (`from app.routers import plan`) para mantener límites claros entre componentes.
- Añade anotaciones de tipo en funciones públicas, dependencias FastAPI y servicios; mantén docstrings breves y orientados a comportamiento.
- Escribe comentarios en español y agrégalos en línea cuando aporten contexto necesario o aclaren lógica no obvia, siguiendo las guías de estilo de Google para comentarios (frases completas, mayúscula inicial, puntuación final).
- Ejecuta `ruff check .` y `black .` antes de commitear si las herramientas están disponibles; centraliza su configuración en `pyproject.toml` cuando se incorporen.

## Guía de Pruebas

- Acompaña cada funcionalidad con pruebas pytest; nombra archivos `test_<feature>.py` y funciones `test_<escenario>`.
- Cubre caminos exitosos, validaciones y bordes para cada endpoint o servicio; apunta a una cobertura mínima del 80% usando `pytest --cov=app`.
- Para lógica con base de datos, utiliza fixtures SQLite en memoria para mantener pruebas determinísticas y rápidas.

## Commits y Pull Requests

- Usa Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, etc.) para titular cada commit; mantén un resumen imperativo de ≤72 caracteres y evita mezclar cambios no relacionados.
- Ejecuta `cz check` antes de abrir el PR para validar el formato y `cz commit` si querés asistencia interactiva.
- En los pull requests incluye resumen, notas de pruebas (comandos ejecutados) y referencias a issues; agrega payloads de ejemplo o capturas cuando cambie la respuesta de la API.

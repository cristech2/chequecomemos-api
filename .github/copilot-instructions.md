# Copilot Instructions for AI Agents

## Normas para Copilot
- Seguir las convenciones de codificación y estilo del proyecto.
- Proporcionar explicaciones claras y concisas para cada función y clase.
- Incluir ejemplos de uso en la documentación.
- Mantener la coherencia en los nombres de las variables y funciones.
- Realizar revisiones de código antes de fusionar cambios.
- Cuando se interactura en el chat no generar directamente el codigo, sino sugerirlo en formato de guias o pasos a seguir.

## Arquitectura y Estructura
- Proyecto backend FastAPI para planificador familiar de comidas ("Che, ¿qué comemos?").
- Estructura modular bajo `app/`:
  - `main.py`: punto de entrada, instancia FastAPI y monta routers.
  - `core/`: configuración global, conexión y sesión de base de datos.
  - `api/`: define routers/endpoints HTTP, sin lógica de negocio ni SQL.
  - `services/`: lógica de negocio, reglas y coordinación de operaciones.
  - `models/`: entidades ORM SQLAlchemy, solo estructura de datos.
  - `schemas/`: modelos Pydantic para entrada/salida, diferenciando crear/actualizar/mostrar.
- Migraciones de base de datos en `alembic/` y configuración en `alembic.ini`.
- Pruebas automáticas en `tests/` (unitarias en `unit/`, integración en `integration/`).

## Flujos de Desarrollo
- Crear entorno virtual: `python -m venv .venv && source .venv/bin/activate`
- Instalar dependencias: `pip install -r requirements.txt`
- Ejecutar servidor: `uvicorn app.main:app --reload`
- Ejecutar pruebas: `pytest` (usar subcarpetas para granularidad)
- Migraciones Alembic:
  - Generar: `alembic revision --autogenerate -m "mensaje"`
  - Aplicar: `alembic upgrade head`

## Convenciones y Patrones
- Commits: Conventional Commits (`feat`, `fix`, `docs`, etc.), resumen ≤72 caracteres, cuerpo opcional.
- Endpoints RESTful claros, ver ejemplos en README.

## Integraciones y Dependencias
- Base de datos SQLite por defecto (local, fuera del repo).
- ORM: SQLModel; migraciones: Alembic.
- Pruebas: Pytest, usar fixtures SQLite en memoria para lógica con BD.
- Documentación interactiva: `/docs` (Swagger UI, FastAPI).

## Ejemplos de Archivos Clave
- `app/main.py`, `app/api/`, `app/services/`, `alembic/`, `tests/`

## Notas
- No multiusuario familiares en MVP, varios usuarios, pero un usuario/una familia.
- Simplificación de unidades y validación de datos iniciales.

---

Para detalles adicionales, consulta `README.md` y `AGENTS.md`. Para instrucciones de python consulta `python.instructions.md`.

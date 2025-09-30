# Repository Guidelines

## Estructura del Proyecto y Organización de Módulos

- Mantén el código de aplicación dentro de `app/`. `main.py` expone la instancia de FastAPI; agrega paquetes como `routers/` para endpoints, `schemas/` para modelos Pydantic, `models/` para entidades ORM y `services/` para la lógica de negocio. Si surge infraestructura compartida, ubícala en `app/core/`.
- Replica la estructura en `tests/` (por ejemplo, `tests/routers/test_plan.py`) y centraliza fixtures comunes en `tests/conftest.py`.
- Gestiona dependencias Python en `requirements.txt`; fija versiones al incorporar librerías nuevas para asegurar despliegues reproducibles.

## Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) - framework backend.
- [Python 3.12+](https://www.python.org/)
- [Uvicorn](https://www.uvicorn.org/) - servidor ASGI.
- [SQLite] - base de datos predeterminada para MVP (local; vive fuera de este repo).
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para gestionar la capa de datos.
- [Alembic](https://alembic.sqlalchemy.org/) - migraciones de esquema versionadas.
- [Pytest](https://docs.pytest.org/) - framework de pruebas unitarias e integrales.
- [Docker] (opcional, para despliegue).

## Estructura del Repositorio (propuesta)

```text
backend/
├─ app/
│  ├─ main.py        # Punto de entrada. Crea la aplicación FastAPI, monta routers y arranca el servidor.
│  │
│  ├─ core/          # Elementos comunes e infraestructura.
│  │                 # Configuración general (variables, conexión DB).
│  │                 # Sesión de base de datos (ciclo de vida por request).
│  │
│  ├─ api/           # Capa de exposición HTTP.
│  │                 # Contiene routers de los recursos.
│  │                 # Solo definen endpoints, validaciones de entrada/salida y códigos de respuesta.
│  │                 # No contienen lógica de negocio ni SQL.
│  │
│  ├─ services/      # Capa de lógica de negocio.
│  │                 # Funciones que aplican reglas y coordinan operaciones.
│  │                 # Llaman a repositorios o directamente a los modelos.
│  │                 # Mantienen las reglas independientes del protocolo HTTP.
│  │
│  ├─ models/        # Capa de persistencia (ORM).
│  │                 # Tablas y relaciones definidas en SQLAlchemy.
│  │                 # No contienen reglas de negocio, solo estructura de datos.
│  │
│  └─ schemas/       # Capa de contratos de datos.
│                    # Definiciones de entrada/salida con Pydantic.
│                    # Diferencian entre crear/actualizar/mostrar.
│
├─ alembic/          # Migraciones versionadas de esquema de base de datos.
├─ alembic.ini       # Configuración de Alembic.
│
└─ tests/            # Pruebas automáticas.
    ├─ unit/         # Pruebas de servicios sin levantar servidor.
    └─ integration/  # Pruebas de endpoints a través de la API.
```

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

- Usa Conventional Commits y asegurá el formato `tipo(scope): resumen` en la primera línea; `scope` es opcional, pero conviene usarlo para identificar módulo o recurso (usa palabras en minúscula separadas por guiones, p. ej. `plan-router`).
- Tipos permitidos en `cz commit`: `fix` (bug; SemVer PATCH), `feat` (feature; SemVer MINOR), `docs` (documentación), `style` (formato sin alterar comportamiento), `refactor` (cambios internos sin nuevas features ni fixes), `perf` (rendimiento), `test` (tests nuevos o corregidos), `build` (build system/dependencias como pip o docker) y `ci` (configuración o scripts de CI como GitLabCI).
- El resumen debe ser imperativo, en minúsculas, sin punto final y ≤72 caracteres; commitizen valida estas reglas al usar la opción `conventional_commit`.
- Tras una línea en blanco, el cuerpo es opcional y sirve para contexto adicional; mantenelo en párrafos cortos generados por `cz commit`.
- Si marcás *Breaking Change* en el asistente, Commitizen antepone `BREAKING CHANGE:` al footer; explica el impacto y pasos de migración allí.
- Usá el footer para referencias (`Refs #123`, `Closes JIRA-45`) o notas de ruptura; el asistente agrega los saltos de línea necesarios.
- Ejecuta `cz check` antes de abrir un PR para validar mensajes existentes y `cz commit` para generar commits siguiendo este flujo.
- En los pull requests incluye resumen, notas de pruebas (comandos ejecutados) y referencias a issues; agrega payloads de ejemplo o capturas cuando cambie la respuesta de la API.

## Formato de Mensajes de Commit

```textplain
tipo(scope): resumen en imperativo

[cuerpo opcional con detalles adicionales]

[BREAKING CHANGE: descripción opcional]
[referencias opcionales]
```

- `scope` puede omitirse; si lo usás, Commitizen normaliza espacios a guiones.
- El cuerpo admite múltiples párrafos separados por líneas en blanco; evitá repetir el resumen.
- Los footers se utilizan para `BREAKING CHANGE:` y referencias cruzadas; Commitizen los agrega al final tras otra línea en blanco.
- Empleá el mismo conjunto de tipos y estructura para mantener consistencia con el changelog automático de Commitizen.

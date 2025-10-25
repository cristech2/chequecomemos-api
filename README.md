
# 🥗 Backend - Planificador Familiar de Comidas
**Nombre comercial:** Che, ¿qué comemos?

API REST construida con **FastAPI** para el MVP del planificador familiar de comidas. Permite gestionar recetas, planificación semanal, inventario y lista de compras consolidada.

---

## 🚀 Objetivo del Proyecto

* Planificar comidas semanales (almuerzo/cena)
* Cargar y consultar recetas manualmente
* Mantener inventario básico de ingredientes
* Generar lista de compras consolidada según el plan y el inventario

---

## ⚙️ Stack Tecnológico

* **FastAPI** (backend, API REST)
* **Python 3.12+**
* **Uvicorn** (servidor ASGI)
* **SQLite** (base de datos local por defecto)
* **SQLModel** (ORM)
* **Alembic** (migraciones de esquema)
* **Pytest** (pruebas unitarias e integrales)
* **Docker** (opcional para despliegue)

---

## 🏗️ Arquitectura y Estructura

El proyecto sigue una estructura modular bajo la carpeta `app/`:

```text
backend/
├─ app/
│  ├─ main.py        # Punto de entrada. Instancia FastAPI y monta routers.
│  ├─ core/          # Configuración global, conexión y sesión de base de datos.
│  ├─ api/           # Routers/endpoints HTTP. Sin lógica de negocio ni SQL.
│  ├─ services/      # Lógica de negocio y coordinación de operaciones.
│  ├─ models/        # Entidades ORM SQLModel y contratos API.
│  └─ schemas/       # Modelos Pydantic para entrada/salida.
├─ alembic/          # Migraciones de base de datos.
├─ alembic.ini       # Configuración Alembic.
└─ tests/            # Pruebas automáticas (unitarias/integración).
```

**Migraciones:**
* Generar: `alembic revision --autogenerate -m "mensaje"`
* Aplicar: `alembic upgrade head`

**Pruebas:**
* Ejecutar: `pytest` (usar subcarpetas para granularidad)

---

## 🧑‍💻 Getting Started

```bash
# Clonar el repositorio
git clone <url_repo>
cd backend

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload
```

Documentación interactiva disponible en:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📅 Endpoints Principales (MVP)

### Planificación
* `GET /plan` → obtener planificación semanal
* `POST /plan` → crear/actualizar comidas para un día (almuerzo/cena)
* `DELETE /plan/{day}/{meal}` → borrar comida planificada

### Recetas
* `GET /recipes` → listar recetas
* `POST /recipes` → crear receta (manual)
* `GET /recipes/{id}` → detalle de receta
* `PUT /recipes/{id}` → editar receta
* `DELETE /recipes/{id}` → eliminar receta

### Inventario
* `GET /inventory` → listar ingredientes (con cantidades/unidades)
* `POST /inventory` → agregar ingrediente
* `PUT /inventory/{id}` → actualizar cantidad/estado (consumido/repuesto)
* `DELETE /inventory/{id}` → eliminar ingrediente

### Lista de compras
* `GET /shopping-list` → generar lista consolidada desde plan + inventario

---

## 🧪 Testing

* Pruebas automáticas con **Pytest**
* Fixtures SQLite en memoria para lógica con BD
* Cobertura mínima recomendada: 80%

---

## 📝 Convenciones y Contribución

* **Estilo de código:** PEP 8, docstrings PEP 257, anotaciones de tipo
* **Commits:** formato convencional (`feat`, `fix`, `docs`, etc.), línea de asunto ≤72 caracteres
* **Pruebas:** unitarias en `tests/unit/`, integración en `tests/integration/`
* **Revisiones:** revisa y documenta cambios antes de fusionar

---

## ⚠️ Notas y Limitaciones

* MVP sin multiusuario familiar (un usuario/familia)
* Simplificación de unidades y validación de datos iniciales
* Inventario inicial depende del usuario

---

## 📚 Referencias y Archivos Clave

* `app/main.py`, `app/api/`, `app/services/`, `alembic/`, `tests/`
* Consulta `AGENTS.md` y `.github/instructions/` para detalles técnicos y convenciones


## 📅 Endpoints (MVP)

### Planificación

- `GET /plan` → obtener planificación semanal
- `POST /plan` → crear/actualizar comidas para un día (almuerzo/cena)
- `DELETE /plan/{day}/{meal}` → borrar comida planificada

### Recetas

- `GET /recipes` → listar recetas
- `POST /recipes` → crear receta (manual)
- `GET /recipes/{id}` → detalle de receta
- `PUT /recipes/{id}` → editar receta
- `DELETE /recipes/{id}` → eliminar receta

### Inventario

- `GET /inventory` → listar ingredientes (con cantidades/unidades)
- `POST /inventory` → agregar ingrediente
- `PUT /inventory/{id}` → actualizar cantidad/estado (consumido/repuesto)
- `DELETE /inventory/{id}` → eliminar ingrediente

### Lista de compras

- `GET /shopping-list` → generar lista consolidada desde plan + inventario

---

## 📊 Métricas de Éxito (MVP)

- Tiempo de planificación semanal (7 días, almuerzo/cena) ≤ **15 min**.
- Lista de compras con al menos **90% de coincidencia** con las recetas planificadas.
- Al menos **1 semana completa** planificada y comprada sin depender de planillas externas.

---

## 📏 Criterios de Hecho

- CRUD básico de recetas.
- Planificación de 7 días (almuerzo/cena).
- Lista de compras generada desde plan + inventario.
- Persistencia básica en BD.
- Inventario editable reflejado en la lista.

---

## ⚠️ Supuestos y Riesgos

- Se trabaja con **un único usuario/familia** (sin roles ni colaboración multiusuario en MVP).
- Conversiones de unidades se simplifican en la primera versión.
- Calidad de datos iniciales del inventario depende del usuario (riesgo de listas incompletas).

---

## 🧪 Ejecución local

```bash
# Clonar repo
git clone <url_repo>
cd backend

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload
```

API docs disponibles en:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

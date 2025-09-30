# 🥗 Backend - Planificador Familiar de Comidas (Nombre Comercial: Che, ¿qué comemos?)

API REST construida con **FastAPI** para el MVP del planificador familiar de comidas.
Permite gestionar **recetas**, **planificación semanal**, **inventario** y la **lista de compras** consolidada.

---

## 🚀 Objetivo del MVP

- Planificar comidas semanales (almuerzo/cena).
- Cargar recetas manualmente y consultarlas.
- Mantener un inventario básico de ingredientes.
- Generar una lista de compras consolidada en base al plan y el inventario.

---

## ⚙️ Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) – framework backend
- [Python 3.12+](https://www.python.org/)
- [Uvicorn](https://www.uvicorn.org/) – servidor ASGI
- [SQLite] – base de datos predeterminada para MVP (local; vive fuera de este repo)
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM para gestionar la capa de datos
- [Alembic](https://alembic.sqlalchemy.org/) – migraciones de esquema versionadas
- [Pytest](https://docs.pytest.org/) – framework de pruebas unitarias e integrales
- [Docker] (opcional, para despliegue)

---

## 📂 Estructura (propuesta)

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

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
- [SQLite] – base de datos predeterminada para MVP (local, simple y portable)
- [Docker] (opcional, para despliegue)

---

## 📂 Estructura (propuesta)

```python
backend/
│── app/
│   ├── main.py          # Punto de entrada FastAPI
│   ├── models/          # Definición ORM
│   ├── routers/         # Endpoints agrupados
│   ├── schemas/         # Pydantic
│   └── services/        # Lógica de negocio
│── tests/               # Pruebas unitarias
│── requirements.txt
│── README.md
```

---

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

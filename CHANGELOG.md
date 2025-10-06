## 0.2.0-alpha (2025-10-05)

### Feat

- **lint**: ajusta la configuración de Ruff y Pytest para mejorar la calidad del código
- **tests**: agrega pruebas unitarias para la creación de usuarios en user_service
- **main**: incluye el enrutador v1 en la aplicación FastAPI
- **users**: agrega endpoints para la gestión de usuarios
- **user_service**: agrega lógica para crear un nuevo usuario en la base de datos
- **schemas**: agrega esquemas Pydantic para la creación y respuesta de usuarios
- **dependencies**: agrega módulo para obtener la sesión de la DB en FastAPI
- **core**: actualiza la exposición de módulos en __init__.py
- **security**: agrega módulo para hashear y verificar contraseñas
- **instructions**: agrega instrucciones para mensajes de commit
- **users-model**: agrega migración inicial y modelo User
- **models**: agregar modelo de usuario
- **config**: agregar archivo de configuración setup.cfg
- **db**: agregar configuración de conexión y ORM
- **alembic**: agregar configuración y scripts de migración

## 0.1.0-alpha (2025-09-30)

### Feat

- **docs**: actualiza la sección de tecnologías y elimina la estructura propuesta del backend
- **database**: crea tabla de usuarios en la base de datos
- **database**: añade modelo de base de datos y justificación para el MVP
- **bootstrap**: se inicializa el backend en FastAPI con configuracion base

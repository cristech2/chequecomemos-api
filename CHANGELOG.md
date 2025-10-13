## 0.3.0-alpha (2025-10-12)

### Feat

- añade colección y entorno de Postman para la API del planificador de comidas
- añade colección y entorno de Postman para la API del planificador de comidas
- refactor modelos y esquemas para usuarios y categorías, actualiza a SQLModel y ajusta la lógica de base de datos
- añade norma para verificar el código mencionado antes de responder
- actualiza el endpoint de registro de usuario para utilizar AsyncSession y mejorar la gestión asíncrona
- refactoriza la función create_user para utilizar SQLModel y AsyncSession
- actualiza las importaciones y el __all__ en el módulo de modelos para incluir las clases de categorías
- renombra la clase Category a CategoryDB para mayor claridad en el modelo de datos
- refactoriza el modelo de categorías para utilizar SQLModel y mejorar la estructura
- refactoriza el modelo de usuario para utilizar SQLModel y simplificar la estructura
- elimina esquemas de usuario y categorías obsoletos
- actualiza la configuración de Alembic para usar SQLModel como metadata
- actualiza la gestión de sesiones de la base de datos a modo asíncrono
- actualiza la conexión a la base de datos para usar SQLAlchemy en modo asíncrono
- actualiza las dependencias a SQLModel y modifica la documentación correspondiente
- agrega esquemas Pydantic para la gestión de categorías
- crea tablas para usuarios y categorías en la base de datos
- agrega modelo para la tabla categories con identificador y nombre únicos
- actualiza la tabla ingredients para referenciar categorías y agrega la tabla categories
- **dev**: agrega pre-commit como dependencia opcional en pyproject.toml
- agrega archivo __init__.py y actualiza metadatos en pyproject.toml

### Fix

- corrige errores tipográficos en la documentación del modelo de usuarios

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

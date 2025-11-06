# AgroGestor - Backend API (Django)

Este repositorio contiene el código fuente del backend para AgroGestor, un sistema web de gestión agrícola desarrollado con Python, Django y Django REST Framework.

La API proporciona un conjunto de endpoints RESTful para gestionar de forma centralizada todas las operaciones de un productor agrícola, desde el inicio de sesión y la gestión de cultivos hasta el análisis de rentabilidad por cosecha. El sistema está diseñado para conectarse a una base de datos Microsoft SQL Server preexistente.

# 🚀 Características Principales

Arquitectura Robusta: Backend monolítico desacoplado con una API RESTful.

Autenticación Segura: Sistema basado en JSON Web Tokens (JWT) con djangorestframework-simplejwt.

Modelo de Usuario Personalizado: Integración de una tabla dbo.Usuarios existente con el sistema AbstractUser de Django, incluyendo un CustomUserManager para manejar ussername como campo de login.

CRUD Completo: Endpoints para Crear, Leer, Actualizar y Desactivar para todos los módulos principales (Cultivos, Suelos, Insumos, Mantenimientos).

Borrado Lógico (Soft Delete): Las peticiones DELETE no borran registros; actualizan el campo estado = False a través de un SoftDeleteViewSetMixin personalizado para proteger la integridad de los datos.

Módulo de Producción y Rentabilidad:

Registro de Cosechas, Ingresos y CostosCosecha.

Endpoint de reporte personalizado (/api/cosechas/<id>/reporte/) que calcula la rentabilidad neta de un ciclo de cultivo.

Integración de API Externa: Un endpoint proxy (/api/weather/) que consulta de forma segura la API de OpenWeatherMap sin exponer la API Key en el frontend.

# 🛠️ Tecnologías Utilizadas

Python 3.10+

Django

Django REST Framework (DRF)

Microsoft SQL Server

mssql-django (Conector de BD)

djangorestframework-simplejwt (Autenticación JWT)

django-cors-headers (Gestión de CORS)

requests (Para peticiones a API externa)

python-decouple (Gestión de variables de entorno)

# 🗂️ Estructura del Proyecto

agrogestor_backend/
├── .venv/                  # Entorno virtual
├── agrogestor_api/         # Núcleo del proyecto Django
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # URLs principales (solo /api/)
│   └── ...
├── gestion/                # App principal con toda la lógica
│   ├── migrations/
│   ├── models.py           # Todos los modelos de la BD (con managed=False)
│   ├── serializers.py      # Todos los serializers
│   ├── views.py            # Todos los ViewSets y la lógica de la API
│   ├── urls.py             # URLs de los endpoints (/cultivos/, /suelos/, etc.)
│   └── ...
├── manage.py               # Script de gestión de Django
├── requirements.txt        # Dependencias de Python
├── .env.example            # Plantilla de variables de entorno
├── .gitignore              # Archivos a ignorar por Git
└── README.md               # Esta documentación


# ⚙️ Instalación y Configuración Local

# 1. Clonar el Repositorio

git clone [https://github.com/alexanderf1000/AgroGestor.Dj.git](https://github.com/alexanderf1000/AgroGestor.Dj.git)
cd AgroGestor.Dj


# 2. Crear y Activar un Entorno Virtual

# Crear el entorno
python -m venv .venv

# Activar en Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activar en Windows (CMD)
.\.venv\Scripts\activate

# Activar en Linux/Mac
source .venv/bin/activate


# 3. Instalar Dependencias

Asegúrate de tener el entorno activado ((venv)) e instala todas las librerías.

pip install -r requirements.txt


# 4. Configurar la Base de Datos (SQL Server)

Este proyecto está diseñado para conectarse a una base de datos preexistente.

Crear la Base de Datos: Asegúrate de que tu instancia de SQL Server tenga una base de datos creada (ej. AgroGestor).

Ejecutar Scripts SQL: Ejecuta los scripts SQL necesarios para crear la estructura de tablas:

creacion de BD y tablas de AgroGestor.sql (para las tablas originales).

El script ALTER TABLE dbo.Usuarios... para añadir las columnas de AbstractUser (password, last_login, is_superuser, is_staff, date_joined).

El script schema_produccion.sql para crear las tablas del módulo de producción (Cosechas, Ingresos, CostosCosecha) y modificar Insumos y MantenimientoCultivos.

# 5. Configurar Variables de Entorno

Crea un archivo llamado .env en la raíz del proyecto.

Copia el contenido de .env.example y rellénalo con tus propios valores. Este archivo debe ser secreto y nunca subirse a GitHub (ya está en .gitignore).

(Revisa agrogestor_api/settings.py para asegurarte de que lee estas variables usando python-decouple).

# 6. Sincronizar Django

Como las tablas ya existen (managed = False), debemos "sincronizar" el historial de migraciones de Django.

# 1. Crear el archivo de migración inicial
python manage.py makemigrations gestion

# 2. "Fingir" que la migración inicial ya fue aplicada
python manage.py migrate --fake-initial


# 7. Crear un Superusuario

Crea un usuario administrador para poder probar el login.

python manage.py createsuperuser


(Te pedirá Ussername gracias a nuestro CustomUserManager).

# 8. Ejecutar el Servidor

python manage.py runserver

# 9.🔌 Endpoints principales (Versión CRUD Completa)
Prefijo de la API: /api/

| Entidad | Método | Endpoint | Acción Principal |
| :--- | :---: | :--- | :--- |
|Autenticación|POST|/api/token/|"Inicia sesión (envía ussername, password)."|
||POST|/api/token/refresh/|Refresca un access token.|
|Usuarios|GET|/api/usuarios/|Listar / Obtener por ID (/{id}/)|
||POST|/api/usuarios/|Crear nuevo usuario|
||PUT|/api/usuarios/<id>/|Actualizar datos|
||DELETE|/api/usuarios/<id>/|Desactivar (Borrado Lógico)|
|Cultivos|GET|/api/cultivos/|Listar / Obtener por ID (/{id}/)|
||POST|/api/cultivos/|Crear nuevo cultivo|
||PUT|/api/cultivos/<id>/|Actualizar datos|
||DELETE|/api/cultivos/<id>/|Desactivar (Borrado Lógico)|
|Suelos|GET|/api/suelos/|Listar / Obtener por ID (/{id}/)|
||POST|/api/suelos/|Crear nuevo suelo|
||PUT|/api/suelos/<id>/|Actualizar datos|
||DELETE|/api/suelos/<id>/|Desactivar (Borrado Lógico)|
|Mantenimientos|GET|/api/mantenimientos/|Listar / Obtener por ID (/{id}/)|
||POST/|api/mantenimientos/|Registrar nueva acción|
||PUT|/api/mantenimientos/<id>/|Actualizar registro|
||DELETE|/api/mantenimientos/<id>/|Desactivar (Borrado Lógico)|
||Insumos|GET|/api/insumos/|Listar / Obtener por ID (/{id}/)|
||POST|/api/insumos/|Agregar nuevo insumo|
||PUT|/api/insumos/<id>/|Actualizar stock/info|
||DELETE|/api/insumos/<id>/|Desactivar (Borrado Lógico)|
|Producción|GET|/api/cosechas/|Listar / Obtener por ID (/{id}/)|
||POST|/api/cosechas/|Crear nueva cosecha|
||GET|/api/ingresos/|Listar / Obtener por ID (/{id}/)|
||POST|/api/ingresos/|Crear nuevo ingreso|
||GET|/api/costos/|Listar / Obtener por ID (/{id}/)|
||POST|/api/costos/|Crear nuevo costo de cosecha|
||GET|/api/cosechas/<id>/reporte/|Obtener Reporte de Rentabilidad|
|Servicios|GET|/api/weather/|Obtener clima (Proxy a OpenWeatherMap)|

# 👤 Autores
Juan Alexander Flores Mairena

Deyling Alejandra Espinoza Montoya

Luis Marcos Acosta Sequeira


# Proyecto desarrollado como proyecto de fin del IV corte de la carrera Ing.En sistemas de información en la universidad (UNAN-Managua).


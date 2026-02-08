# Energy Process - Sistema de Procesamiento de Energía

## Reporte de Actividades

**Fecha:** __/__/____  
**Semana:** __ – Configuración inicial del proyecto  
**Rol:** _____  
**Responsable:** ______

---

### 1. Actividades realizadas

Durante este periodo se realizó la preparación completa del entorno local de desarrollo, incluyendo:

- Configuración del repositorio Git local
- Estructura inicial del proyecto con arquitectura de microservicios
- Configuración de Docker y Docker Compose para orquestación de servicios
- Implementación del backend con FastAPI (Python)
- Implementación del frontend con React + Vite
- Configuración de worker con Celery para procesamiento asíncrono
- Configuración de base de datos PostgreSQL
- Configuración de Redis para caché y cola de tareas
- Implementación de migraciones de base de datos con Alembic
- Configuración de variables de entorno
- Estructura de carpetas y archivos base del proyecto

---

### 2. Entregables generados

#### Backend (FastAPI)
- [`backend/app/main.py`](backend/app/main.py) - Aplicación principal FastAPI
- [`backend/app/config.py`](backend/app/config.py) - Configuración de la aplicación
- [`backend/app/database.py`](backend/app/database.py) - Configuración de base de datos
- [`backend/app/celery_app.py`](backend/app/celery_app.py) - Configuración de Celery
- [`backend/app/tasks.py`](backend/app/tasks.py) - Tareas asíncronas

**Modelos de datos:**
- [`backend/app/models/archivo_procesado.py`](backend/app/models/archivo_procesado.py)
- [`backend/app/models/energia_excedentaria.py`](backend/app/models/energia_excedentaria.py)
- [`backend/app/models/registro_errores.py`](backend/app/models/registro_errores.py)
- [`backend/app/models/tipo_autoconsumo.py`](backend/app/models/tipo_autoconsumo.py)

**Rutas API:**
- [`backend/app/api/routes/archivos.py`](backend/app/api/routes/archivos.py) - Gestión de archivos
- [`backend/app/api/routes/energia.py`](backend/app/api/routes/energia.py) - Consulta de energía
- [`backend/app/api/routes/errores.py`](backend/app/api/routes/errores.py) - Gestión de errores
- [`backend/app/api/routes/stats.py`](backend/app/api/routes/stats.py) - Estadísticas

**Servicios:**
- [`backend/app/services/archivo_service.py`](backend/app/services/archivo_service.py)
- [`backend/app/services/procesador_service.py`](backend/app/services/procesador_service.py)

**Migraciones:**
- [`backend/migrations/versions/001_initial_schema.py`](backend/migrations/versions/001_initial_schema.py)

**Tests:**
- [`backend/tests/test_api_endpoints.py`](backend/tests/test_api_endpoints.py)
- [`backend/tests/test_parsing.py`](backend/tests/test_parsing.py)

#### Frontend (React + Vite)
- [`frontend/src/main.jsx`](frontend/src/main.jsx) - Punto de entrada
- [`frontend/src/App.jsx`](frontend/src/App.jsx) - Componente principal
- [`frontend/index.html`](frontend/index.html) - HTML base

**Componentes:**
- [`frontend/src/components/FileUpload.jsx`](frontend/src/components/FileUpload.jsx)
- [`frontend/src/components/EnergiaList.jsx`](frontend/src/components/EnergiaList.jsx)
- [`frontend/src/components/ErrorDisplay.jsx`](frontend/src/components/ErrorDisplay.jsx)
- [`frontend/src/components/Layout.jsx`](frontend/src/components/Layout.jsx)

**Páginas:**
- [`frontend/src/pages/Home.jsx`](frontend/src/pages/Home.jsx)
- [`frontend/src/pages/Carga.jsx`](frontend/src/pages/Carga.jsx)
- [`frontend/src/pages/Consulta.jsx`](frontend/src/pages/Consulta.jsx)
- [`frontend/src/pages/Archivos.jsx`](frontend/src/pages/Archivos.jsx)
- [`frontend/src/pages/Dashboard.jsx`](frontend/src/pages/Dashboard.jsx)

**Servicios:**
- [`frontend/src/services/api.js`](frontend/src/services/api.js) - Cliente API

#### Infraestructura
- [`docker-compose.yml`](docker-compose.yml) - Orquestación de servicios
- [`backend/Dockerfile`](backend/Dockerfile) - Imagen Docker del backend
- [`frontend/Dockerfile`](frontend/Dockerfile) - Imagen Docker del frontend
- [`worker/Dockerfile`](worker/Dockerfile) - Imagen Docker del worker
- [`.env`](.env) - Variables de entorno
- [`backend/requirements.txt`](backend/requirements.txt) - Dependencias Python
- [`frontend/package.json`](frontend/package.json) - Dependencias Node.js

#### Documentación
- [`README.md`](README.md) - Este documento
- [`resq.rest`](resq.rest) - Ejemplos de peticiones HTTP

---

### 3. Incidencias

**Sin incidencias**

El entorno de desarrollo se configuró exitosamente. El repositorio está listo para ser subido a GitHub.

---

## Instrucciones de Uso

### Requisitos previos
- Docker y Docker Compose instalados
- Git instalado
- Node.js (para desarrollo local del frontend)
- Python 3.11+ (para desarrollo local del backend)

### Configuración inicial

1. **Clonar el repositorio** (una vez subido a GitHub):
```bash
git clone <URL_DEL_REPOSITORIO>
cd Energy_Process
```

2. **Configurar variables de entorno**:
   - Revisar y ajustar el archivo [`.env`](.env) según sea necesario

3. **Levantar los servicios con Docker**:
```bash
docker-compose up -d
```

4. **Ejecutar migraciones de base de datos**:
```bash
docker-compose exec backend alembic upgrade head
```

### Acceso a los servicios

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentación API (Swagger)**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Desarrollo local

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Ejecutar tests

```bash
docker-compose exec backend pytest
```

---

## Arquitectura del Proyecto

```
Energy_Process/
├── backend/          # API FastAPI + Celery worker
│   ├── app/
│   │   ├── api/      # Rutas y endpoints
│   │   ├── models/   # Modelos de base de datos
│   │   ├── schemas/  # Esquemas Pydantic
│   │   ├── services/ # Lógica de negocio

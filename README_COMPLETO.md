# 🔋 Energy Process - Sistema de Procesamiento de Energía Excedentaria

**Versión:** 1.0.0  
**Última actualización:** Febrero 2026

---

## 📋 Tabla de Contenidos

1. [Descripción General del Proyecto](#descripción-general-del-proyecto)
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Instalación y Configuración](#instalación-y-configuración)
6. [Descripción de Módulos y Rutas](#descripción-de-módulos-y-rutas)
7. [Clasificación de CUPS](#clasificación-de-cups)
8. [Procesamiento de Archivos](#procesamiento-de-archivos)
9. [Modelos de Datos](#modelos-de-datos)
10. [Flujo de Procesamiento](#flujo-de-procesamiento)
11. [APIs REST](#apis-rest)
12. [Ejecución y Testing](#ejecución-y-testing)

---

## 🎯 Descripción General del Proyecto

**Energy Process** es un sistema de procesamiento y gestión de energía excedentaria de instalaciones de autoconsumo. El sistema permite:

- **Carga de archivos**: Upload de archivos en múltiples formatos (CSV, XML, TXT)
- **Validación automática**: Verificación de integridad de datos y CUPS
- **Procesamiento asíncrono**: Uso de Celery para procesar archivos sin bloquear la API
- **Gestión de errores**: Registro detallado de errores por línea de archivo
- **Consultas flexibles**: API REST para búsqueda y filtrado de datos
- **Detección de duplicados**: Prevención de procesamiento de archivos duplicados mediante hash SHA256

### Casos de Uso Principales

1. **Usuarios cargando archivos de energía excedentaria** → El sistema valida y procesa automáticamente
2. **Consulta de registros procesados** → Búsqueda por CUPS, fechas, tipo de autoconsumo
3. **Análisis de errores** → Visualizar qué datos fallaron y por qué
4. **Estadísticas del sistema** → Resumen de procesamiento

---

## 🛠️ Tecnologías Utilizadas

### Backend

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **FastAPI** | 0.109.0+ | Framework web moderno, rápido y type-safe |
| **SQLAlchemy** | 2.0.0+ | ORM para interacción con base de datos |
| **Pydantic** | 2.5.0+ | Validación de esquemas y datos |
| **Celery** | 5.3.0+ | Cola de tareas asincrónicas |
| **Redis** | 5.0.0+ | Broker de mensajes para Celery |
| **PostgreSQL** | 15-Alpine | Base de datos relacional |
| **Alembic** | 1.13.0+ | Migraciones de base de datos |
| **Uvicorn** | 0.27.0+ | Servidor ASGI |
| **Pytest** | 7.4.0+ | Framework de testing |
| **Python** | 3.9+ | Lenguaje principal |

### Frontend

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **React** | 18.2.0+ | Librería de UI interactiva |
| **React Router DOM** | 6.21.0+ | Enrutamiento en SPA |
| **Vite** | 5.0.10+ | Build tool y dev server ultrarrápido |
| **Axios** | 1.6.2+ | Cliente HTTP para consumir APIs |
| **CSS Puro** | - | Estilos sin dependencias adicionales |

### Infraestructura

| Componente | Tecnología | Propósito |
|-----------|-----------|----------|
| **Contenedorización** | Docker & Docker Compose | Despliegue consistente |
| **Base de Datos** | PostgreSQL 15 | Almacenamiento persistente |
| **Cola de Tareas** | Redis + Celery | Procesamiento asincrónico |
| **API Gateway** | CORS de FastAPI | Control de acceso |

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE FINAL (Navegador)                 │
│                          (Frontend)                           │
└──────────────────────────┬──────────────────────────┘
                           │ HTTP/REST
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│              SERVIDOR API (FastAPI Backend)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Rutas HTTP                                          │   │
│  │  - POST /api/v1/archivos/upload     (Upload)         │   │
│  │  - GET  /api/v1/archivos            (List)           │   │
│  │  - GET  /api/v1/archivos/{id}       (Status)         │   │
│  │  - GET  /api/v1/energia             (Query)          │   │
│  │  - GET  /api/v1/errores/{archivo}   (Errors)         │   │
│  │  - GET  /api/v1/stats               (Statistics)     │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                   │
│          ┌────────────────┼────────────────┐                 │
│          ▼                ▼                ▼                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Servicios    │  │ Validadores  │  │ Middleware   │       │
│  │ - Procesa    │  │ - CUPS       │  │ - CORS       │       │
│  │ - Transforma │  │ - Fechas     │  │ - Auth       │       │
│  │ - Valida     │  │ - Números    │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│          │                                                     │
└──────────┼─────────────────────────────────────────────────────┘
           │ ORM SQLAlchemy
           ▼
    ┌──────────────────────┐
    │   PostgreSQL 15      │
    │   - archivo_procesado│
    │   - energia_excedentaria
    │   - registro_errores │
    │   - cliente          │
    │   - usuario          │
    └──────────────────────┘

PROCESAMIENTO ASINCRÓNICO:

FastAPI encolá tarea → Redis (Broker) → Celery Worker
                        ↓
                  procesar_archivo()
                        ↓
              Actualizar en PostgreSQL
```

### Componentes Principales

1. **API REST (FastAPI)**: Recibe peticiones HTTP, valida datos, gestiona sesiones de BD
2. **Servicios**: Lógica de negocio (procesador_service.py, archivo_service.py)
3. **Validadores**: Reglas de validación (CUPS, tipos, fechas, números)
4. **Modelos**: Representación de tablas en base de datos
5. **Esquemas**: Validación y serialización con Pydantic
6. **Celery Worker**: Procesa archivos asincronicamente
7. **PostgreSQL**: Almacenamiento persistente
8. **Redis**: Broker de mensajes y caché

---

## 📁 Estructura del Proyecto

```
Energy_Process/
│
├── README.md                          # README original
├── README_COMPLETO.md                 # Este documento
├── docker-compose.yml                 # Orquestación de servicios
├── resq.rest                          # Cliente REST para pruebas
│
├── backend/                           # 🔧 API FastAPI + Lógica
│   ├── Dockerfile                     # Imagen Docker del backend
│   ├── Makefile                       # Comandos útiles
│   ├── requirements.txt               # Dependencias Python
│   ├── start_dev.sh                   # Script de inicio desarrollo
│   ├── alembic.ini                    # Configuración de migraciones
│   │
│   ├── app/                           # Aplicación principal
│   │   ├── __init__.py
│   │   ├── main.py                    # Punto de entrada FastAPI
│   │   ├── config.py                  # Configuración de app
│   │   ├── database.py                # Conexión SQLAlchemy
│   │   ├── celery_app.py              # Configuración de Celery
│   │   ├── tasks.py                   # Tareas asincrónicas
│   │   │
│   │   ├── api/                       # 🔌 Rutas HTTP
│   │   │   ├── deps.py                # Dependencias comunes
│   │   │   └── routes/
│   │   │       ├── archivos.py        # Upload, list, status
│   │   │       ├── energia.py         # Consultas de registros
│   │   │       ├── errores.py         # Consultas de errores
│   │   │       ├── stats.py           # Estadísticas
│   │   │       ├── auth.py            # Autenticación (comentado)
│   │   │       ├── usuarios.py        # Gestión de usuarios (comentado)
│   │   │       └── clientes.py        # Gestión de clientes (comentado)
│   │   │
│   │   ├── models/                    # 🗄️ ORM SQLAlchemy
│   │   │   ├── archivo_procesado.py   # Tabla de archivos
│   │   │   ├── energia_excedentaria.py# Tabla de energía
│   │   │   ├── registro_errores.py    # Tabla de errores
│   │   │   ├── tipo_autoconsumo.py    # Tabla de tipos
│   │   │   ├── cliente.py             # Cliente (relación)
│   │   │   └── usuario.py             # Usuario (relación)
│   │   │
│   │   ├── schemas/                   # 📋 Validación Pydantic
│   │   │   ├── archivo.py             # DTOs para archivos
│   │   │   ├── energia.py             # DTOs para energía
│   │   │   ├── error.py               # DTOs para errores
│   │   │   ├── auth.py                # DTOs para auth (comentado)
│   │   │   ├── usuario.py             # DTOs para usuarios (comentado)
│   │   │   └── cliente.py             # DTOs para clientes (comentado)
│   │   │
│   │   ├── services/                  # ⚙️ Lógica de Negocio
│   │   │   ├── procesador_service.py  # Parsing, validación, inserción
│   │   │   └── archivo_service.py     # Gestión de archivos
│   │   │
│   │   └── utils/                     # 🛠️ Funciones Auxiliares
│   │       ├── validators.py          # Validadores personalizados
│   │       └── auth.py                # Funciones de autenticación (comentado)
│   │
│   ├── migrations/                    # 📚 Migraciones Alembic
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 001_initial_schema.py
│   │
│   ├── tests/                         # 🧪 Tests
│   │   ├── conftest.py
│   │   ├── test_api_endpoints.py
│   │   └── test_parsing.py
│   │
│   └── uploads/                       # 📤 Archivos subidos temporalmente
│
├── frontend/                          # 🎨 UI React + Vite
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   │
│   └── src/
│       ├── main.jsx                   # Punto de entrada
│       ├── App.jsx                    # Componente raíz
│       ├── index.css
│       │
│       ├── components/                # 🧩 Componentes Reutilizables
│       │   ├── Layout.jsx             # Layout general
│       │   ├── FileUpload.jsx         # Carga de archivos
│       │   ├── DataViewer.jsx         # Visualización de datos
│       │   ├── EnergiaList.jsx        # Listado de registros
│       │   └── ErrorDisplay.jsx       # Visualización de errores
│       │
│       ├── pages/                     # 📄 Páginas (Vistas)
│       │   ├── Home.jsx
│       │   ├── Carga.jsx              # Page de carga
│       │   ├── Consulta.jsx           # Page de consulta
│       │   ├── Archivos.jsx           # Page de archivos
│       │   ├── Dashboard.jsx          # Page de estadísticas
│       │   ├── Clientes.jsx           # Page de clientes (comentado)
│       │   ├── Usuarios.jsx           # Page de usuarios (comentado)
│       │   └── Login.jsx              # Page de login (comentado)
│       │
│       ├── services/                  # 🌐 Servicios HTTP
│       │   └── api.js                 # Cliente axios
│       │
│       └── context/                   # 🔐 Context API
│           └── AuthContext.jsx        # Contexto de autenticación
│
└── worker/                            # ⚙️ Worker Celery Standalone
    └── Dockerfile
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Docker** y **Docker Compose** instalados
- **Git** para clonar el repositorio
- **Node.js** 18+ (para desarrollo local frontend)
- **Python** 3.9+ (para desarrollo local backend)

### Opción 1: Con Docker Compose (Recomendado)

```bash
# Clonar repositorio
git clone <URL_DEL_REPO>
cd Energy_Process

# Crear archivo .env (opcional)
cat > .env << EOF
POSTGRES_USER=postgres
POSTGRES_PASSWORD=0823
POSTGRES_DB=energy_process
ENVIRONMENT=development
VITE_API_URL=http://localhost:8000
EOF

# Levantar todos los servicios
docker-compose up -d

# Ejecutar migraciones (primera vez)
docker-compose exec backend alembic upgrade head

# Verificar que todo está corriendo
docker-compose ps
```

**Acceso a servicios:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Opción 2: Desarrollo Local

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar PostgreSQL localmente o usar docker compose para BD
# docker-compose up -d postgres redis

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload

# En otra terminal: Iniciar worker Celery
cd ../
celery -A app.celery_app worker -l info
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar dev server
npm run dev

# Build para producción
npm run build

# Preview de build
npm run preview
```

---

## 📡 Descripción de Módulos y Rutas

### 1. Backend - Rutas API

#### **Módulo: `archivos.py`** - Gestión de Archivos

```python
POST /api/v1/archivos/upload
```
- **Descripción**: Sube un archivo para procesamiento
- **Parámetros**:
  - `file` (UploadFile): Archivo CSV, XML o TXT
  - `usuario_id` (int, opcional): ID del usuario (default: 1)
- **Respuesta**:
  ```json
  {
    "archivo_id": 1,
    "nombre_archivo": "peajes_2024.csv",
    "estado": "pendiente",
    "mensaje": "Archivo en cola de procesamiento"
  }
  ```
- **Validaciones**:
  - Calcula SHA256 del archivo para detectar duplicados
  - Rechaza si archivo ya fue procesado antes
  - Guarda en carpeta `uploads/`

```python
GET /api/v1/archivos
```
- **Descripción**: Lista todos los archivos procesados
- **Parámetros**:
  - `limit` (int, 1-100): Cantidad de resultados (default: 20)
- **Respuesta**:
  ```json
  [
    {
      "id": 1,
      "usuario_id": 1,
      "nombre_archivo": "peajes.csv",
      "estado": "completado",
      "total_registros": 150,
      "registros_exitosos": 140,
      "registros_con_error": 10,
      "fecha_carga": "2024-02-05T10:30:00",
      "fecha_procesamiento": "2024-02-05T10:35:00"
    }
  ]
  ```

```python
GET /api/v1/archivos/{archivo_id}
```
- **Descripción**: Consulta estado de un archivo específico
- **Respuesta**: Mismo modelo que lista (un solo objeto)

---

#### **Módulo: `energia.py`** - Consulta de Registros

```python
GET /api/v1/energia
```
- **Descripción**: Consulta registros de energía con filtros avanzados
- **Parámetros opcionales**:
  - `cups` (str): Código CUPS del cliente (ej: ES1234567890)
  - `fecha_desde` (date): Filtro fecha inicio (YYYY-MM-DD)
  - `fecha_hasta` (date): Filtro fecha fin (YYYY-MM-DD)
  - `tipo_autoconsumo` (int): Tipo [12, 41, 42, 43, 51]
- **Respuesta**:
  ```json
  {
    "total": 2,
    "registros": [
      {
        "id": 1,
        "cups_cliente": "ES1234567890",
        "instalacion_gen": "AUT-001",
        "tipo_autoconsumo": 12,
        "fecha_desde": "2024-01-01",
        "fecha_hasta": "2024-01-31",
        "energia_neta_gen": [100.5, 101.2, 99.8, 102.1, 100.9, 101.3],
        "energia_autoconsumida": [50.2, 49.8, 51.1, 50.5, 50.9, 49.6],
        "pago_tda": [12.50, 12.45, 12.78, 12.63, 12.72, 12.40]
      }
    ]
  }
  ```

---

#### **Módulo: `errores.py`** - Gestión de Errores

```python
GET /api/v1/errores
```
- **Descripción**: Obtiene todos los errores del sistema
- **Respuesta**:
  ```json
  [
    {
      "id": 1,
      "archivo_id": 1,
      "linea_archivo": 5,
      "tipo_error": "cliente_inexistente",
      "descripcion": "CUPS ES9999999999 no encontrado en sistema",
      "datos_linea": "{\"cups_cliente\": \"ES9999999999\", ...}",
      "fecha_registro": "2024-02-05T10:35:30"
    }
  ]
  ```

```python
GET /api/v1/errores/{archivo_id}
```
- **Descripción**: Obtiene errores de un archivo específico
- **Respuesta**: Lista de errores del archivo

---

#### **Módulo: `stats.py`** - Estadísticas

```python
GET /api/v1/stats
```
- **Descripción**: Resumen general de procesamiento
- **Respuesta**:
  ```json
  {
    "total_archivos": 10,
    "archivos_completados": 9,
    "archivos_con_error": 1,
    "total_registros": 5000,
    "registros_exitosos": 4850,
    "registros_con_error": 150
  }
  ```

---

### 2. Frontend - Componentes y Páginas

#### **Componentes Reutilizables**

| Componente | Archivo | Funcionalidad |
|-----------|---------|---------------|
| **Layout** | `Layout.jsx` | Estructura general, header, navegación |
| **FileUpload** | `FileUpload.jsx` | Formulario drag-drop para cargar archivos |
| **DataViewer** | `DataViewer.jsx` | Tabla con datos y paginación |
| **EnergiaList** | `EnergiaList.jsx` | Listado de registros de energía |
| **ErrorDisplay** | `ErrorDisplay.jsx` | Visualización de errores con detalles |

#### **Páginas (Vistas)**

| Página | Ruta | Función |
|-------|------|---------|
| **Home** | `/` | Página de inicio y bienvenida |
| **Carga** | `/carga` | Cargar archivos nuevos |
| **Consulta** | `/consulta` | Búsqueda avanzada de registros |
| **Archivos** | `/archivos` | Historial de archivos procesados |
| **Dashboard** | `/dashboard` | Estadísticas del sistema |

#### **Servicio HTTP**

**`services/api.js`** - Cliente Axios centralizado

```javascript
// Ejemplos de uso
api.uploadFile(file)          // POST upload
api.listArchivos()            // GET archivos
api.getArchivoStatus(id)      // GET archivo/{id}
api.queryEnergia(filters)     // GET energia con filtros
api.getErrores(archivoId)     // GET errores
api.getStats()                // GET stats
```

---

## 🎯 Clasificación de CUPS

### ¿Qué es un CUPS?

**CUPS** = Código Único de Punto de Suministro  
Identificador único nacional de 20-22 caracteres para cada punto de suministro eléctrico en España.

### Estructura del CUPS

```
ES 1234 12 12 X 1234567890 A
│  │    │  │  │ │          │
│  │    │  │  │ │          └─ Dígito de control (A-J)
│  │    │  │  │ │
│  │    │  │  │ └──────────── Número de suministro (10 dígitos)
│  │    │  │  │
│  │    │  │  └────────────── Tipo de consumidor (X)
│  │    │  │
│  │    │  └──────────────── Municipio (2 dígitos)
│  │    │
│  │    └────────────────── Provincia (2 dígitos)
│  │
│  └─────────────────────── Distribuidora (4 dígitos)
│
└─────────────────────────── País (ES = España)
```

### Validación de CUPS en el Sistema

```python
# Función en: backend/app/services/procesador_service.py

def validar_cups_existe(cups: str, db: Session) -> bool:
    """
    Verifica si CUPS existe.
    - Actualmente: Simulado con validación básica
    - Validación: Debe comenzar con 'ES' y tener >= 10 caracteres
    - Mejora futura: Consultar tabla 'cliente' para verificación real
    """
    return bool(cups and cups.startswith("ES") and len(cups) >= 10)
```

### Proceso de Clasificación

**Flujo:**

1. **Extracción**: Se lee el campo `cups_cliente` de cada línea del archivo
2. **Trim**: Se eliminan espacios en blanco (`strip()`)
3. **Validación básica**: 
   - No está vacío
   - Comienza con "ES"
   - Longitud >= 10 caracteres
4. **Validación avanzada** (Futuro):
   - Verificar que existe en tabla `cliente`
   - Validar dígito de control
5. **Resultado**:
   - ✅ VALID: Se procesa el registro
   - ❌ ERROR: Se registra en tabla `registro_errores` con tipo `cliente_inexistente`

### Tipos de Errores relacionados a CUPS

| Tipo de Error | Descripción | Ejemplo |
|---------------|-------------|---------|
| `cliente_inexistente` | CUPS no encontrado | "ES9999999999 no encontrado en sistema" |
| `formato_invalido` | CUPS mal formateado | "CUPS vacío o malformado" |

---

## 📊 Procesamiento de Archivos

### Formatos Soportados

| Formato | Extensión | Codificación | Estructura |
|---------|-----------|-------------|-----------|
| **CSV** | `.csv` | UTF-8 | Columnas delimitadas por comas |
| **XML** | `.xml` | UTF-8 | Parsing con ElementTree (futuro) |
| **TXT** | `.txt` | UTF-8 | Delimitado por tabulaciones o espacios |

**Nota**: Actualmente solo se implementó CSV. XML y TXT necesitan adaptadores.

### Estructura de Archivo CSV Esperada

```csv
cups_cliente,instalacion_gen,fecha_desde_1,fecha_hasta_1,tipo_autoconsumo,energia_neta_gen_1,energia_neta_gen_2,energia_neta_gen_3,energia_neta_gen_4,energia_neta_gen_5,energia_neta_gen_6,energia_autoconsumida_1,energia_autoconsumida_2,energia_autoconsumida_3,energia_autoconsumida_4,energia_autoconsumida_5,energia_autoconsumida_6,pago_tda_1,pago_tda_2,pago_tda_3,pago_tda_4,pago_tda_5,pago_tda_6
ES1234567890,AUT-001,2024-01-01,2024-01-31,12,100.5,101.2,99.8,102.1,100.9,101.3,50.2,49.8,51.1,50.5,50.9,49.6,12.50,12.45,12.78,12.63,12.72,12.40
```

### Columnas Requeridas

| Columna | Tipo | Rango | Descripción |
|---------|------|-------|-------------|
| `cups_cliente` | String | - | Código CUPS del cliente |
| `instalacion_gen` | String | - | ID de instalación generadora |
| `fecha_desde_1` | Date | YYYY-MM-DD | Fecha inicio de período |
| `fecha_hasta_1` | Date | YYYY-MM-DD | Fecha fin de período |
| `tipo_autoconsumo` | Integer | {12,41,42,43,51} | Tipo de autoconsumo |
| `energia_neta_gen_1..6` | Decimal | +0.000 | Energía neta gen por período (P1-P6) |
| `energia_autoconsumida_1..6` | Decimal | +0.000 | Energía autoconsumida (P1-P6) |
| `pago_tda_1..6` | Decimal | +0.00 | Pago TDA en euros (P1-P6) |

### Tipos de Autoconsumo Válidos

```python
# backend/app/utils/validators.py

TIPOS_AUTOCONSUMO_VALIDOS = {12, 41, 42, 43, 51}

# Descripción de cada tipo (según normativa):
# 12: Autoconsumo sin excedentes
# 41: Autoconsumo con excedentes - Modalidad B (compensación)
# 42: Autoconsumo con excedentes - Modalidad B (venta)
# 43: Autoconsumo con excedentes - Modalidad B (almacenamiento)
# 51: Consumo propios con generación
```

### Proceso Paso a Paso

```
1. RECEPCIÓN
   ├─ Usuario sube archivo vía POST /api/v1/archivos/upload
   ├─ Se calcula SHA256 del contenido
   └─ Se verifica que no sea duplicado

2. ALMACENAMIENTO
   ├─ Se guarda en carpeta ./uploads/
   ├─ Se crea registro ArchivoProcesado con estado="pendiente"
   └─ Se retorna archivo_id al cliente

3. ENCOLAMIENTO
   ├─ Se encola tarea Celery con (archivo_id, ruta_archivo)
   ├─ Función: app.tasks.procesar_archivo_task()
   └─ Redis almacena la tarea en cola

4. PROCESAMIENTO (Celery Worker)
   ├─ Worker obtiene tarea de Redis
   ├─ Cambia estado a "procesando"
   ├─ Abre archivo CSV y lee línea por línea
   └─ Para cada línea:
      │
      ├─ VALIDACIÓN
      │  ├─ Valida CUPS (existe, formato)
      │  ├─ Valida Tipo (12, 41, 42, 43, 51)
      │  ├─ Valida Fechas (formato YYYY-MM-DD, hasta >= desde)
      │  ├─ Valida Arrays (exactamente 6 valores numéricos cada uno)
      │  └─ Valida Números (conversión a Decimal válida)
      │
      ├─ SI ERRORES
      │  ├─ Registra error en RegistroErrores
      │  ├─ Incrementa contador con_error
      │  └─ Continúa con siguiente línea
      │
      └─ SI OK
         ├─ Inserta en EnergiaExcedentaria
         ├─ Incrementa contador exitosos
         └─ Continúa

5. FINALIZACIÓN
   ├─ Se actualiza estado a "completado" (o "error" si falla)
   ├─ Se guarda: total_registros, registros_exitosos, registros_con_error
   ├─ Se guarda: fecha_procesamiento
   └─ Cliente puede consultar resultados
```

### Validaciones Detalladas

#### 1. Validación de CUPS

```python
def validar_cups(cups: str) -> bool:
    cups = cups.strip()
    return bool(cups and cups.startswith("ES") and len(cups) >= 10)

# Errores posibles:
# - "CUPS ES9999999999 no encontrado en sistema" → cliente_inexistente
```

#### 2. Validación de Tipo Autoconsumo

```python
# Debe estar en {12, 41, 42, 43, 51}
if tipo not in TIPOS_AUTOCONSUMO_VALIDOS:
    # Error: tipo_no_soportado

# Ejemplos:
# Tipo 12 ✓ Válido
# Tipo 99 ✗ Error: "Tipo autoconsumo 99 no válido"
```

#### 3. Validación de Fechas

```python
# Formato requerido: YYYY-MM-DD
from datetime import datetime

fecha_desde = datetime.strptime("2024-01-01", "%Y-%m-%d")  # ✓
fecha_desde = datetime.strptime("01/01/2024", "%Y-%m-%d")  # ✗ ValueError

# Además: fecha_hasta >= fecha_desde
```

#### 4. Validación de Arrays (P1-P6)

```python
# Cada campo debe tener exactamente 6 valores:
energia_neta_gen_1, ..., energia_neta_gen_6

# Cada valor debe ser convertible a Decimal
Decimal("100.5")    # ✓
Decimal("abc")      # ✗ InvalidOperation
```

#### 5. Validación de Números

```python
from decimal import Decimal, InvalidOperation

try:
    valor = Decimal(str(campo).strip())
except InvalidOperation:
    # Error: formato_invalido
```

### Tipos de Errores Registrados

| Tipo de Error | Descripción | Causa |
|---------------|-------------|-------|
| `cliente_inexistente` | CUPS no encontrado | CUPS no comienza con "ES" o < 10 chars |
| `tipo_no_soportado` | Tipo autoconsumo inválido | No está en {12,41,42,43,51} |
| `formato_invalido` | Formato de dato incorrecto | Fecha mala, número no convertible |
| `fecha_invalida` | Fechas con formato incorrecto | No es YYYY-MM-DD |
| `array_longitud_invalida` | Array sin 6 elementos | energia_neta_gen no tiene 6 valores |
| `archivo_duplicado` | Archivo ya fue procesado | Hash SHA256 existe |
| `inconsistencia_numerica` | Error al insertar en BD | Overflow o constraint violation |

---

## 🗄️ Modelos de Datos

### Diagrama de Relaciones

```
┌─────────────────────┐
│      usuario        │
├─────────────────────┤
│ id (PK)             │
│ nombre              │
│ email               │
└────────────┬────────┘
             │
             │ 1:N
             ▼
┌─────────────────────────────┐
│    archivo_procesado        │
├─────────────────────────────┤
│ id (PK)                     │
│ usuario_id (FK)             │
│ nombre_archivo              │
│ hash_archivo (UNIQUE)       │
│ estado                      │
│ fecha_carga                 │
│ fecha_procesamiento         │
│ total_registros             │
│ registros_exitosos          │
│ registros_con_error         │
│ ruta_archivo                │
└────┬──────────────────┬─────┘
     │                  │
     │ 1:N              │ 1:N
     ▼                  ▼
┌───────────────────────┐  ┌──────────────────────┐
│ energia_excedentaria  │  │  registro_errores    │
├───────────────────────┤  ├──────────────────────┤
│ id (PK)               │  │ id (PK)              │
│ archivo_id (FK)       │  │ archivo_id (FK)      │
│ cliente_id (FK)       │  │ linea_archivo        │
│ linea_archivo         │  │ tipo_error           │
│ instalacion_gen       │  │ descripcion          │
│ fecha_desde           │  │ datos_linea          │
│ fecha_hasta           │  │ fecha_registro       │
│ tipo_autoconsumo (FK) │  └──────────────────────┘
│ energia_neta_gen[]    │
│ energia_autoconsumida[]
│ pago_tda[]            │
│ fecha_creacion        │
└───────┬─────┬─────────┘
        │     │
        │     │ N:1
        │     ▼
        │  ┌──────────────────────┐
        │  │  cliente             │
        │  ├──────────────────────┤
        │  │ id (PK)              │
        │  │ cups_cliente         │
        │  │ nombre               │
        │  └──────────────────────┘
        │
        │ N:1
        ▼
    ┌──────────────────────┐
    │  tipo_autoconsumo    │
    ├──────────────────────┤
    │ codigo (PK) {12..51} │
    │ descripcion          │
    │ activo               │
    └──────────────────────┘
```

### Tablas Principales

#### **1. `archivo_procesado`**

```python
class ArchivoProcesado(Base):
    __tablename__ = "archivo_procesado"

    id: Integer (PK)                    # ID único autoincremental
    usuario_id: Integer (FK)            # Referencia a usuario
    nombre_archivo: String(255)         # "peajes_2024.csv"
    hash_archivo: String(64)            # SHA256 único
    fecha_carga: DateTime               # Cuándo se subió
    fecha_procesamiento: DateTime       # Cuándo se procesó
    estado: String(20)                  # Estado {pendiente, procesando, completado, error}
    total_registros: Integer            # Total líneas leídas
    registros_exitosos: Integer         # Líneas procesadas OK
    registros_con_error: Integer        # Líneas con error
    ruta_archivo: Text                  # Ubicación archivo
```

**Restricciones:**
```sql
CHECK (estado IN ('pendiente', 'procesando', 'completado', 'error'))
UNIQUE (hash_archivo)
```

#### **2. `energia_excedentaria`**

```python
class EnergiaExcedentaria(Base):
    __tablename__ = "energia_excedentaria"

    id: Integer (PK)                    # ID único
    archivo_id: Integer (FK)            # De qué archivo viene
    cliente_id: Integer (FK)            # Cliente propietario
    linea_archivo: Integer              # Número de línea en CSV
    instalacion_gen: String(50)         # ID instalación
    fecha_desde: Date                   # Inicio período
    fecha_hasta: Date                   # Fin período
    tipo_autoconsumo: Integer (FK)      # {12, 41, 42, 43, 51}
    energia_neta_gen: Array[Decimal]    # 6 valores (P1-P6)
    energia_autoconsumida: Array[Decimal] # 6 valores (P1-P6)
    pago_tda: Array[Decimal]            # 6 valores (P1-P6)
    fecha_creacion: DateTime            # Cuándo se insertó
```

**Restricciones:**
```sql
FOREIGN KEY (archivo_id) REFERENCES archivo_procesado ON DELETE CASCADE
FOREIGN KEY (cliente_id) REFERENCES cliente ON DELETE RESTRICT
FOREIGN KEY (tipo_autoconsumo) REFERENCES tipo_autoconsumo
CHECK (fecha_hasta >= fecha_desde)
```

#### **3. `registro_errores`**

```python
class RegistroErrores(Base):
    __tablename__ = "registro_errores"

    id: Integer (PK)                    # ID único
    archivo_id: Integer (FK)            # Archivo donde falló
    linea_archivo: Integer              # Número de línea
    tipo_error: String(50)              # Tipo error (ej: cliente_inexistente)
    descripcion: Text                   # Descripción detallada
    datos_linea: Text (JSON)            # Datos de la línea que falló
    fecha_registro: DateTime            # Cuándo se registró error
```

**Restricciones:**
```sql
FOREIGN KEY (archivo_id) REFERENCES archivo_procesado ON DELETE CASCADE
CHECK (tipo_error IN (
    'cliente_inexistente', 'tipo_no_soportado', 'formato_invalido',
    'archivo_duplicado', 'inconsistencia_numerica',
    'array_longitud_invalida', 'fecha_invalida'
))
```

#### **4. `tipo_autoconsumo`**

```python
class TipoAutoconsumo(Base):
    __tablename__ = "tipo_autoconsumo"

    codigo: Integer (PK)                # {12, 41, 42, 43, 51}
    descripcion: String(255)            # Descripción del tipo
    activo: Boolean                     # Disponible o no
```

**Restricciones:**
```sql
CHECK (codigo IN (12, 41, 42, 43, 51))
```

---

## 🔄 Flujo de Procesamiento Completo

### Vista General del Flujo

```
USUARIO               FRONTEND              BACKEND API              WORKER (Celery)         BD (PostgreSQL)
   │                    │                        │                         │                      │
   ├─ Click Upload ─────►│                        │                         │                      │
   │                    │─ POST /upload ────────►│                         │                      │
   │                    │  (archivo)            │                         │                      │
   │                    │                       ├─ Hash SHA256             │                      │
   │                    │                       ├─ Verificar duplicado ───────────────────────►│
   │                    │                       │◄─────────────────────────────────────────────│
   │                    │                       ├─ Guardar en uploads/     │                      │
   │                    │                       ├─ INSERT archivo_procesado ────────────────────►│
   │                    │                       │◄─────────────────────────────────────────────│
   │                    │◄─ 202 Accepted ──────│                         │                      │
   │                    │  {archivo_id: 1}     ├─ Encolar en Celery      │                      │
   │                    │                       │──────────────────────────►│                      │
   │                    │                       │                         │                      │
   │ (Usuario espera)   │                       │                         ├─ Obtener tarea      │
   │                    │                       │                         │                      │
   │                    │ GET /archivos/1 ─────►│                         │                      │
   │                    │  (check status)       ├─ SELECT * FROM archivo_procesado ────────────►│
   │                    │◄─ {estado: procesando}│◄─────────────────────────────────────────────│
   │                    │                       │                         │ UPDATE estado='procesando'
   │                    │                       │                         │ Abre archivo       │
   │                    │                       │                         │ Lee línea 1:       │
   │                    │                       │                         │                    │
   │                    │                       │                         ├─ Validar CUPS ────►│
   │                    │                       │                         │ ✓ ES1234567890    │
   │                    │                       │                         ├─ Validar tipo ────►│
   │                    │                       │                         │ ✓ Tipo 12        │
   │                    │                       │                         ├─ Validar fechas ──►│
   │                    │                       │                         │ ✓ 2024-01-01..31  │
   │                    │                       │                         ├─ Validar arrays ──►│
   │                    │                       │                         │ ✓ 6 valores cada  │
   │                    │                       │                         │                    │
   │                    │                       │                         ├─ INSERT energia_excedentaria ──┐
   │                    │                       │                         │◄──────────────────────────────┤
   │                    │                       │                         │ Éxito incrementa exitosos     │
   │                    │                       │                         │                               │
   │                    │                       │                         │ Lee línea 2: CUPS inválido   │
   │                    │                       │                         ├─ INSERT registro_errores ────┐
   │                    │                       │                         │◄──────────────────────────────┤
   │                    │                       │                         │ Error incrementa con_error   │
   │                    │                       │                         │                               │
   │                    │                       │                         │ ... más líneas ...           │
   │                    │                       │                         │                               │
   │                    │                       │                         ├─ UPDATE archivo completado ──┐
   │                    │                       │                         │◄──────────────────────────────┤
   │                    │                       │                         │ total_registros: 150         │
   │                    │                       │                         │ registros_exitosos: 140      │
   │                    │                       │                         │ registros_con_error: 10      │
   │                    │ GET /archivos/1 ─────►│                         │                               │
   │                    │  (check status again) ├─ SELECT * FROM archivo_procesado ────────────────►│
   │                    │◄─ {estado: completado}│◄──────────────────────────────────────────────────│
   │                    │  exitosos: 140        │                         │                               │
   │                    │  errores: 10          │                         │                               │
   │                    │                       │                         │                               │
   │ (Vista resultados) │                       │                         │                               │
   │◄────────────────────────────────────────────────────────────────────────────────────────────────────
```

### Secuencia Detallada

#### **Fase 1: Upload y Encolamiento**

```python
# 1. Usuario envía archivo
POST /api/v1/archivos/upload
  Content-Type: multipart/form-data
  file: <contenido_del_archivo>

# 2. Backend recibe y calcula hash
contenido = await file.read()
hash_archivo = hashlib.sha256(contenido).hexdigest()

# 3. Verifica duplicado
archivo_existente = obtener_archivo_por_hash(db, hash_archivo)
if archivo_existente:
    raise HTTPException(400, "Archivo duplicado")

# 4. Guarda archivo en disco
upload_dir = Path(settings.UPLOAD_DIR)
ruta_guardado = upload_dir / file.filename
ruta_guardado.write_bytes(contenido)

# 5. Crea registro en BD
nuevo_archivo = ArchivoProcesado(
    usuario_id=usuario_id,
    nombre_archivo=file.filename,
    hash_archivo=hash_archivo,
    estado="pendiente",
    ruta_archivo=str(ruta_guardado)
)
db.add(nuevo_archivo)
db.commit()
db.refresh(nuevo_archivo)

# 6. Encola tarea Celery
procesar_archivo_task.delay(nuevo_archivo.id, str(ruta_guardado))

# 7. Retorna respuesta 202 ACCEPTED
return {
    "archivo_id": nuevo_archivo.id,
    "estado": "pendiente",
    "mensaje": "Archivo en cola de procesamiento"
}
```

#### **Fase 2: Procesamiento Asincrónico**

```python
# app/tasks.py
@celery_app.task(bind=True, name="procesar_archivo")
def procesar_archivo_task(self, archivo_id: int, ruta_archivo: str):
    db = SessionLocal()
    try:
        procesar_archivo(db, archivo_id, ruta_archivo)
    finally:
        db.close()

# app/services/procesador_service.py
def procesar_archivo(db: Session, archivo_id: int, ruta_archivo: str):
    
    # 1. Obtiene objeto archivo
    archivo = db.query(ArchivoProcesado).filter(...).first()
    
    # 2. Cambia estado a procesando
    archivo.estado = "procesando"
    archivo.fecha_procesamiento = datetime.utcnow()
    db.commit()
    
    # 3. Abre archivo CSV
    exitosos = 0
    con_error = 0
    total = 0
    
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for num_linea, row in enumerate(reader, start=2):
            total += 1
            
            # 4. Limpia espacios en datos
            row = {k.strip(): v for k, v in row.items() if k}
            
            # 5. VALIDA LÍNEA
            errores = validar_linea(row, num_linea, db)
            
            # 6. Si hay errores
            if errores:
                for tipo_err, desc in errores:
                    registrar_error(
                        db, archivo_id, num_linea,
                        tipo_err, desc, json.dumps(row)
                    )
                con_error += 1
            
            # 7. Si OK, inserta
            else:
                try:
                    insertar_energia(db, archivo_id, num_linea, row)
                    exitosos += 1
                except Exception as e:
                    registrar_error(
                        db, archivo_id, num_linea,
                        "inconsistencia_numerica", str(e), json.dumps(row)
                    )
                    con_error += 1
    
    # 8. Actualiza estado final
    archivo.estado = "completado"
    archivo.total_registros = total
    archivo.registros_exitosos = exitosos
    archivo.registros_con_error = con_error
    db.commit()
```

---

## 🌐 APIs REST

### Autenticación

**Actualmente**: Deshabilitada (usuario_id hardcodeado a 1)  
**Futuro**: JWT tokens, roles de usuario

### Endpoints Resumen

```
┌──────────────────────────────────────────────────────────────┐
│                    ARCHIVOS ENDPOINTS                         │
├──────────────────────────────────────────────────────────────┤
│ POST   /api/v1/archivos/upload          │ Sube archivo       │
│ GET    /api/v1/archivos                 │ Lista archivos     │
│ GET    /api/v1/archivos/{id}            │ Status de archivo  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    ENERGÍA ENDPOINTS                          │
├──────────────────────────────────────────────────────────────┤
│ GET    /api/v1/energia                  │ Consulta registros │
│        - ?cups=...                      │ (con filtros)      │
│        - ?fecha_desde=...               │                    │
│        - ?fecha_hasta=...               │                    │
│        - ?tipo_autoconsumo=...          │                    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    ERRORES ENDPOINTS                          │
├──────────────────────────────────────────────────────────────┤
│ GET    /api/v1/errores                  │ Todos los errores  │
│ GET    /api/v1/errores/{archivo_id}     │ Errores archivo    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    STATS ENDPOINTS                            │
├──────────────────────────────────────────────────────────────┤
│ GET    /api/v1/stats                    │ Estadísticas       │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    DOCS ENDPOINT                              │
├──────────────────────────────────────────────────────────────┤
│ GET    /docs                            │ Swagger UI         │
│ GET    /redoc                           │ ReDoc              │
└──────────────────────────────────────────────────────────────┘
```

### Request/Response Examples

#### Upload Archivo

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/archivos/upload \
  -F "file=@peajes.csv"
```

**Response (202 Accepted):**
```json
{
  "archivo_id": 1,
  "nombre_archivo": "peajes.csv",
  "estado": "pendiente",
  "mensaje": "Archivo en cola de procesamiento"
}
```

#### List Archivos

**Request:**
```bash
curl http://localhost:8000/api/v1/archivos?limit=10
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "usuario_id": 1,
    "nombre_archivo": "peajes.csv",
    "hash_archivo": "abc123...",
    "fecha_carga": "2024-02-05T10:30:00",
    "fecha_procesamiento": "2024-02-05T10:35:00",
    "estado": "completado",
    "total_registros": 150,
    "registros_exitosos": 140,
    "registros_con_error": 10,
    "ruta_archivo": "./uploads/peajes.csv"
  }
]
```

#### Consulta Energía con Filtros

**Request:**
```bash
curl "http://localhost:8000/api/v1/energia?cups=ES1234567890&tipo_autoconsumo=12"
```

**Response (200 OK):**
```json
{
  "total": 5,
  "registros": [
    {
      "id": 1,
      "archivo_id": 1,
      "cups_cliente": "ES1234567890",
      "instalacion_gen": "AUT-001",
      "tipo_autoconsumo": 12,
      "fecha_desde": "2024-01-01",
      "fecha_hasta": "2024-01-31",
      "energia_neta_gen": [100.5, 101.2, 99.8, 102.1, 100.9, 101.3],
      "energia_autoconsumida": [50.2, 49.8, 51.1, 50.5, 50.9, 49.6],
      "pago_tda": [12.50, 12.45, 12.78, 12.63, 12.72, 12.40],
      "fecha_creacion": "2024-02-05T10:35:30"
    }
  ]
}
```

---

## 🧪 Ejecución y Testing

### Iniciar Sistema

**Con Docker Compose (Recomendado):**
```bash
docker-compose up -d

# Ver logs
docker-compose logs -f backend
docker-compose logs -f worker

# Acceder a servicios
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Swagger: http://localhost:8000/docs
```

**Development Local:**

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Terminal 2 - Worker:
```bash
cd backend
source venv/bin/activate
celery -A app.celery_app worker -l info
```

Terminal 3 - Frontend:
```bash
cd frontend
npm run dev
```

### Ejecutar Tests

```bash
# Con Docker
docker-compose exec backend pytest

# Local
cd backend
pytest -v
pytest tests/test_parsing.py -v
pytest tests/test_api_endpoints.py -v

# Con coverage
pytest --cov=app tests/
```

### Migraciones de Base de Datos

```bash
# Crear nueva migración
alembic revision --autogenerate -m "Descripción cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver estado
alembic current
alembic history
```

### Pruebas Manuales con Cliente HTTP

**Archivo `resq.rest` (REST Client):**

```http
### Upload archivo
POST http://localhost:8000/api/v1/archivos/upload
Content-Type: multipart/form-data

file=@./test_files/peajes.csv

### List archivos
GET http://localhost:8000/api/v1/archivos?limit=5

### Get archivo status
GET http://localhost:8000/api/v1/archivos/1

### Consulta energía
GET http://localhost:8000/api/v1/energia?cups=ES1234567890&tipo_autoconsumo=12

### Get errores
GET http://localhost:8000/api/v1/errores/1

### Estadísticas
GET http://localhost:8000/api/v1/stats

### Swagger docs
GET http://localhost:8000/docs
```

---

## 📈 Monitoreo y Debugging

### Ver Logs del Sistema

```bash
# Backend
docker-compose logs -f backend

# Worker Celery
docker-compose logs -f worker

# PostgreSQL
docker-compose logs -f postgres

# Redis
docker-compose logs -f redis

# Todos
docker-compose logs -f
```

### Verificar Estado de Servicios

```bash
# Listar contenedores
docker-compose ps

# Inspeccionar redis
redis-cli PING
redis-cli KEYS "*"

# Conectar a PostgreSQL
psql postgresql://postgres:0823@localhost:5432/energy_process

# Queries útiles
SELECT * FROM archivo_procesado ORDER BY fecha_carga DESC LIMIT 5;
SELECT * FROM energia_excedentaria WHERE archivo_id = 1;
SELECT * FROM registro_errores WHERE archivo_id = 1;
```

### Debugging

```python
# Backend: Habilitar logs SQL
# En database.py cambiar:
echo=False  → echo=True  # Ver todas las queries SQL

# Celery: Ver tareas en cola
celery -A app.celery_app inspect active
celery -A app.celery_app inspect scheduled
celery -A app.celery_app purge  # Limpiar cola (cuidado!)
```

---

## 🔒 Consideraciones de Seguridad

### Implementado

- ✅ **Hash SHA256** para detectar duplicados de archivos
- ✅ **SQL Injection Prevention** mediante ORM (SQLAlchemy)
- ✅ **CORS enabled** con whitelist de orígenes
- ✅ **Validación de entrada** exhaustiva (CUPS, fechas, tipos)
- ✅ **Type hints** con Pydantic para validación de datos

### Pendiente de Implementar

- ⚠️ **Autenticación JWT** para usuarios
- ⚠️ **HTTPS/SSL** en producción
- ⚠️ **Rate limiting** en endpoints
- ⚠️ **Encriptación de contraseñas** (bcrypt)
- ⚠️ **Sanitización de datos** en formularios
- ⚠️ **Auditoría de acceso** (quién subió qué archivo)
- ⚠️ **Permisos por rol** (admin, usuario normal)

---

## 🚀 Deployment a Producción

### Requisitos Previos

1. **Servidor** con Docker y Docker Compose
2. **Dominio** apuntando al servidor
3. **Certificado SSL** (Let's Encrypt)
4. **Backups** configurados

### Checklist de Producción

```bash
# 1. Variables de entorno
export ENVIRONMENT=production
export CORS_ORIGINS=https://example.com
export DATABASE_URL=postgresql://user:pass@prod-db:5432/energy_prod

# 2. Escalado de workers
# docker-compose scale worker=3

# 3. Nginx proxy reverso
# Configurar SSL, rate limiting, cache

# 4. Monitoreo
# Prometheus, Grafana, Sentry para errores

# 5. Logs centralizados
# ELK stack o CloudWatch

# 6. Backups automáticos
# Cron jobs para PostgreSQL dumps

# 7. Health checks
# GET /health endpoint
```

---

## 📚 Recursos Adicionales

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

## ❓ Preguntas Frecuentes

**P: ¿Qué pasa si un archivo se procesa dos veces?**  
R: El sistema lo detecta por el hash SHA256 y rechaza la carga con un error 400.

**P: ¿Cuánto tarda en procesarse un archivo?**  
R: Depende del tamaño. Típicamente: 1000 registros = 5-10 segundos.

**P: ¿Puedo cancelar un procesamiento en curso?**  
R: Sí, purgando la tarea Celery: `celery -A app.celery_app purge`

**P: ¿Qué sucede si la BD se cae durante el procesamiento?**  
R: El registro de archivo queda en estado "procesando" y hay registros parciales.

**P: ¿Dónde se guardan los archivos?**  
R: En carpeta `./uploads/` (puede configurarse en `.env`).

**P: ¿Es necesario tener Redis para funcionar?**  
R: No obligatorio. Si falla Celery, el sistema procesa sincronamente en el API.

---

## 👨‍💻 Información de Contacto / Mantenimiento

**Desarrollador**: Sitko  
**Versión**: 1.0.0  
**Última actualización**: Febrero 2026

---

**FIN DEL DOCUMENTO**
